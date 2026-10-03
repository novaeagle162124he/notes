"""Reusable helper functions for working with notes."""

import re
import unicodedata
from collections.abc import Iterable


def normalize_note_text(text: str) -> str:
    """Normalize line endings, trailing whitespace, and excessive blank lines."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    normalized = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", normalized)


def create_note_slug(title: str) -> str:
    """Convert a note title into a lowercase, URL-friendly ASCII slug."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    return slug or "untitled"


def normalize_tags(tags: Iterable[str]) -> list[str]:
    """Normalize, deduplicate, and return non-empty note tags in input order."""
    normalized_tags: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        normalized = re.sub(r"\s+", " ", tag).strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            normalized_tags.append(normalized)

    return normalized_tags


def create_excerpt(content: str, max_length: int = 160) -> str:
    """Create a single-line excerpt without exceeding the requested length."""
    if max_length < 1:
        raise ValueError("max_length must be at least 1")

    normalized = re.sub(r"\s+", " ", content).strip()
    if len(normalized) <= max_length:
        return normalized
    if max_length == 1:
        return "…"

    available_length = max_length - 1
    candidate = normalized[:available_length]
    word_boundary = candidate.rfind(" ")
    if word_boundary > 0:
        candidate = candidate[:word_boundary]

    return candidate.rstrip() + "…"