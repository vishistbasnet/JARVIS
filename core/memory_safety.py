"""
Safety checks for persistent JARVIS memories.
"""

from __future__ import annotations

import re


SENSITIVE_PATTERNS = (
    r"\bapi[_ -]?key\b",
    r"\bpassword\b",
    r"\bpasswd\b",
    r"\bsecret\b",
    r"\baccess[_ -]?token\b",
    r"\bauth[_ -]?token\b",
    r"\bprivate[_ -]?key\b",
    r"\bbearer\s+token\b",
)


def is_safe_memory(content: str) -> bool:
    """Return True when content is safe to persist."""

    text = content.strip()

    if not text:
        return False

    return not any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in SENSITIVE_PATTERNS
    )