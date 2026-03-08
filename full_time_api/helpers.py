"""String helpers."""

import re


def remove_whitespace(text: str) -> str:
    """Trim and normalize whitespace: single spaces, no newlines."""
    trimmed = text.strip()
    normalized = trimmed.replace("\n", "").replace("\r", "")
    return re.sub(r"\s+", " ", normalized)
