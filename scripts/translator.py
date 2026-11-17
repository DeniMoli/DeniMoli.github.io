import logging
import re
import time

from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Google Translate has a ~5000 char limit per request
CHUNK_SIZE = 4500


def _translate(text: str, source: str = "auto") -> str:
    if not text.strip():
        return text
    translator = GoogleTranslator(source=source, target="ru")
    if len(text) <= CHUNK_SIZE:
        return translator.translate(text)
    # Split into chunks on paragraph boundaries
    chunks = _split_chunks(text, CHUNK_SIZE)
    translated = []
    for chunk in chunks:
        translated.append(translator.translate(chunk))
        time.sleep(0.3)  # avoid rate limiting
    return "\n\n".join(translated)


def _split_chunks(text: str, max_len: int) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    current_len = 0
    for para in paragraphs:
        if current_len + len(para) > max_len and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def _extract_code_blocks(text: str) -> tuple[str, dict]:
    """Replace code blocks with placeholders to avoid translating code."""
    placeholders = {}
    counter = [0]

    def replace(match):
        key = f"__CODE_BLOCK_{counter[0]}__"
        placeholders[key] = match.group(0)
        counter[0] += 1
        return key

    # Fenced code blocks (``` or ~~~)
    text = re.sub(r"```[\s\S]*?```", replace, text)
    text = re.sub(r"~~~[\s\S]*?~~~", replace, text)
    # Inline code
    text = re.sub(r"`[^`\n]+`", replace, text)
    return text, placeholders


def _restore_code_blocks(text: str, placeholders: dict) -> str:
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def translate_markdown(markdown: str) -> str:
    """Translate markdown body from English to Russian, preserving code blocks."""
    text, placeholders = _extract_code_blocks(markdown)
    translated = _translate(text)
    return _restore_code_blocks(translated, placeholders)


def translate_fields(title: str, description: str) -> tuple[str, str]:
    """Translate title and description fields."""
    try:
        ru_title = _translate(title)
        ru_desc = _translate(description)
        return ru_title, ru_desc
    except Exception as e:
        logger.warning(f"Failed to translate fields: {e}")
        return title, description
