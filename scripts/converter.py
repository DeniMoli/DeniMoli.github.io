import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse

from markdownify import markdownify as md

from fetcher import ArticleCandidate
from scraper import ScrapedArticle, download_og_image
from translator import translate_fields, translate_markdown

logger = logging.getLogger(__name__)


@dataclass
class BlogPostFile:
    filename: str
    frontmatter: str
    body: str
    image_path: str
    files_to_add: list[str] = field(default_factory=list)


def _clean_markdown(text: str) -> str:
    """Remove common blog chrome that survives HTML extraction."""
    lines = text.splitlines()
    cleaned = []
    skip_section = False

    # Headings that signal non-content sections
    chrome_headings = {
        "последние статьи", "более свежие статьи", "recent posts", "related posts",
        "more articles", "newer entries", "older entries", "ежемесячный брифинг",
        "monthly briefing", "tags", "теги", "about the author", "об авторе",
        "subscribe", "подписаться", "comments", "комментарии",
    }

    for line in lines:
        stripped = line.strip()

        # Detect chrome section headings and skip until next heading
        if stripped.startswith("#"):
            heading_text = stripped.lstrip("#").strip().lower()
            if heading_text in chrome_headings:
                skip_section = True
                continue
            else:
                skip_section = False

        if skip_section:
            continue

        # Skip lines that are pure archive year links: [2024](/2024/)
        if re.match(r"^[-–—]?\s*\[20\d\d\]\(/20\d\d/\)\s*$", stripped):
            continue

        # Skip sponsor/support lines
        if re.match(r"^\*\*при поддержке", stripped.lower()):
            continue

        cleaned.append(line)

    text = "\n".join(cleaned)
    # Collapse 3+ newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_to_markdown(html: str) -> str:
    text = md(html, heading_style="ATX", bullets="-")
    # Remove leading/trailing whitespace per line
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    return _clean_markdown(text)


def make_slug(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    segment = path.split("/")[-1] if path else ""
    # Remove numeric prefixes and file extensions
    segment = re.sub(r"\.\w+$", "", segment)
    segment = re.sub(r"^\d+-?", "", segment)
    # Keep only URL-safe chars
    slug = re.sub(r"[^a-z0-9-]", "-", segment.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
    return slug or "post"


def make_tags(rss_tags: list[str], source_name: str) -> list[str]:
    seen = set()
    result = []
    for tag in rss_tags:
        normalized = tag.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
        if len(result) == 5:
            break
    if not result:
        result = [source_name.lower().split()[0]]
    return result


def _build_frontmatter(title: str, date: str, description: str,
                        image_path: str, tags: list[str]) -> str:
    # Escape any colons in title/description that would break YAML
    safe_title = title.replace('"', '\\"')
    safe_desc = description.replace('"', '\\"')
    tags_json = json.dumps(tags, ensure_ascii=False)
    return (
        f'---\n'
        f'title: "{safe_title}"\n'
        f'date: {date}\n'
        f'description: "{safe_desc}"\n'
        f'image: {image_path}\n'
        f'alt: "{safe_title}"\n'
        f'ogImage: {image_path}\n'
        f'tags: {tags_json}\n'
        f'published: true\n'
        f'---'
    )


def build_post_file(
    scraped: ScrapedArticle,
    candidate: ArticleCandidate,
    next_num: int,
    config: dict,
) -> BlogPostFile:
    slug = make_slug(candidate.url)
    date = datetime.now().strftime("%d.%m.%Y")
    tags = make_tags(scraped.tags, candidate.source_name)
    body = html_to_markdown(scraped.html_body)

    title = scraped.title
    description = scraped.description[:160]

    # Translate English articles to Russian
    if scraped.language == "en":
        logger.info(f"Translating article to Russian: {title[:60]}")
        title, description = translate_fields(title, description)
        body = translate_markdown(body)

    # Append source reference
    body = body + f"\n\n---\n\n**Источник:** [{scraped.title}]({scraped.url})"

    # Resolve image
    files_to_add: list[str] = []
    image_path = config["images"]["fallback"]

    if scraped.og_image_url:
        downloaded = download_og_image(scraped.og_image_url, slug, config)
        if downloaded:
            image_path = downloaded
            # Track the local file path for git add
            rel_path = f"{config['images']['output_dir']}{slug}" + image_path[image_path.rfind("."):]
            files_to_add.append(rel_path)

    frontmatter = _build_frontmatter(
        title=title,
        date=date,
        description=description,
        image_path=image_path,
        tags=tags,
    )
    filename = f"{next_num}. {slug}.md"

    return BlogPostFile(
        filename=filename,
        frontmatter=frontmatter,
        body=body,
        image_path=image_path,
        files_to_add=files_to_add,
    )
