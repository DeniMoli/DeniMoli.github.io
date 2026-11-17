import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone

import feedparser

from state import is_duplicate

logger = logging.getLogger(__name__)


@dataclass
class ArticleCandidate:
    url: str
    title: str
    summary: str
    source_name: str
    source_language: str
    published_at: datetime
    rss_tags: list[str] = field(default_factory=list)
    relevance_score: float = 0.0


def _parse_date(entry) -> datetime:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def _word_count(text: str) -> int:
    return len(text.split())


def score_relevance(candidate: ArticleCandidate, topics: list[str]) -> float:
    if not topics:
        return 1.0
    haystack = (candidate.title + " " + candidate.summary).lower()
    matches = sum(1 for t in topics if t.lower() in haystack)
    return matches / len(topics)


def fetch_feed(source: dict, config: dict) -> list[ArticleCandidate]:
    url = source["url"]
    name = source["name"]
    language = source.get("language", "en")
    min_words = config["pipeline"]["min_word_count"]

    logger.info(f"Fetching feed: {name} ({url})")
    feed = feedparser.parse(url)

    candidates = []
    for entry in feed.entries:
        import re
        link = getattr(entry, "link", None)
        title = getattr(entry, "title", "").strip()
        # feedparser maps <content:encoded> to entry.content[0].value
        # and <description> to entry.summary — try both
        summary = getattr(entry, "summary", "") or ""
        if not summary and hasattr(entry, "content") and entry.content:
            summary = entry.content[0].get("value", "")
        clean_summary = re.sub(r"<[^>]+>", " ", summary).strip()

        if not link or not title:
            continue
        # RSS summaries are always short excerpts; just skip completely empty ones
        if _word_count(clean_summary) < 30:
            continue

        rss_tags = [tag.term.lower().strip() for tag in getattr(entry, "tags", [])
                    if hasattr(tag, "term") and tag.term]

        candidates.append(ArticleCandidate(
            url=link,
            title=title,
            summary=clean_summary,
            source_name=name,
            source_language=language,
            published_at=_parse_date(entry),
            rss_tags=rss_tags,
        ))

    logger.info(f"{name}: {len(candidates)} candidate(s) after length filter")
    return candidates


def fetch_all_sources(config: dict, state: dict) -> list[ArticleCandidate]:
    sources = [s for s in config["sources"] if s.get("enabled", True)]
    global_topics = config["topics"]["global"]
    max_articles = config["pipeline"]["max_articles_per_run"]

    all_candidates: list[ArticleCandidate] = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_source = {
            executor.submit(fetch_feed, source, config): source
            for source in sources
        }
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                candidates = future.result()
            except Exception as e:
                logger.warning(f"Failed to fetch {source['name']}: {e}")
                continue

            source_topics = source.get("topics") or global_topics

            for candidate in candidates:
                if is_duplicate(candidate.url, state):
                    continue
                candidate.relevance_score = score_relevance(candidate, source_topics)
                if candidate.relevance_score > 0:
                    all_candidates.append(candidate)

    all_candidates.sort(
        key=lambda c: (c.relevance_score, c.published_at.timestamp()),
        reverse=True,
    )

    result = all_candidates[:max_articles]
    logger.info(f"Total candidates after filtering: {len(result)}")
    return result
