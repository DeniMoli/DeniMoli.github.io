import logging
import mimetypes
import os
import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from fetcher import ArticleCandidate

logger = logging.getLogger(__name__)


class ScrapeError(Exception):
    pass


@dataclass
class ScrapedArticle:
    url: str
    title: str
    description: str
    og_image_url: Optional[str]
    html_body: str
    tags: list[str] = field(default_factory=list)
    language: str = "en"


def _get_meta(soup: BeautifulSoup, *names: str) -> str:
    for name in names:
        tag = (
            soup.find("meta", property=name)
            or soup.find("meta", attrs={"name": name})
        )
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def _absolutize_urls(html: str, base_url: str) -> str:
    """Replace relative img src and a href with absolute URLs using base_url."""
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith(("http://", "https://", "data:")):
            img["src"] = urljoin(base_url, src)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href and not href.startswith(("http://", "https://", "mailto:", "#")):
            a["href"] = urljoin(base_url, href)
    return str(soup)


def _extract_body(soup: BeautifulSoup) -> str:
    # Remove noisy semantic elements first
    for tag in soup.find_all(["script", "style", "iframe", "noscript",
                               "header", "footer", "nav", "aside",
                               "form", "button"]):
        tag.decompose()

    # Remove elements with class/id names that indicate blog chrome
    chrome_keywords = [
        "sponsor", "subscribe", "newsletter", "archive", "tag-cloud", "tags",
        "related", "sidebar", "widget", "advertisement", "promo", "banner",
        "recent-posts", "more-posts", "pagination", "breadcrumb", "social",
        "share", "comment", "author-bio", "signup", "cta",
    ]
    for kw in chrome_keywords:
        for el in soup.find_all(class_=lambda c, k=kw: c and k in " ".join(c).lower()):
            el.decompose()
        for el in soup.find_all(id=lambda i, k=kw: i and k in i.lower()):
            el.decompose()

    # Try semantic containers in priority order
    selectors = [
        "article",
        "[class*='post-content']",
        "[class*='article-content']",
        "[class*='entry-content']",
        "[class*='article-body']",
        "[id='content']",
        "[class='content']",
        "main",
    ]
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            # Remove any remaining chrome inside the selected container
            for tag in el.find_all(["header", "footer", "nav", "aside"]):
                tag.decompose()
            return str(el)

    # Fallback: body without header/footer/nav
    body = soup.find("body")
    return str(body) if body else ""


def scrape_article(candidate: ArticleCandidate, config: dict) -> ScrapedArticle:
    headers = {"User-Agent": config["pipeline"]["user_agent"]}
    timeout = config["pipeline"]["request_timeout"]

    try:
        resp = requests.get(candidate.url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ScrapeError(f"HTTP error for {candidate.url}: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")

    title = (
        _get_meta(soup, "og:title")
        or (soup.find("h1").get_text(strip=True) if soup.find("h1") else "")
        or candidate.title
    )
    description = (
        _get_meta(soup, "og:description", "description")
        or candidate.summary[:200]
    )
    og_image = _get_meta(soup, "og:image") or None
    if og_image and not og_image.startswith("http"):
        og_image = urljoin(candidate.url, og_image)

    html_body = _extract_body(soup)
    if not html_body.strip():
        raise ScrapeError(f"Could not extract body from {candidate.url}")
    html_body = _absolutize_urls(html_body, candidate.url)

    # Merge RSS tags with article:tag meta tags
    article_tags = [
        t["content"].lower().strip()
        for t in soup.find_all("meta", attrs={"property": "article:tag"})
        if t.get("content")
    ]
    tags = list(dict.fromkeys(candidate.rss_tags + article_tags))  # deduplicate, preserve order

    return ScrapedArticle(
        url=candidate.url,
        title=title,
        description=description,
        og_image_url=og_image,
        html_body=html_body,
        tags=tags,
        language=candidate.source_language,
    )


def download_og_image(image_url: str, slug: str, config: dict) -> Optional[str]:
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        config["images"]["output_dir"],
    )
    headers = {"User-Agent": config["pipeline"]["user_agent"]}
    timeout = config["pipeline"]["request_timeout"]

    try:
        resp = requests.get(image_url, headers=headers, timeout=timeout, stream=True)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        ext = mimetypes.guess_extension(content_type) or ".jpg"
        # Normalize common aliases
        ext = {".jpe": ".jpg", ".jpeg": ".jpg"}.get(ext, ext)

        filename = f"{slug}{ext}"
        output_path = os.path.join(output_dir, filename)

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Downloaded image: {filename}")
        return f"/blogs-img/{filename}"

    except Exception as e:
        logger.warning(f"Failed to download image {image_url}: {e}")
        return None
