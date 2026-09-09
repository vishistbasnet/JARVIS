"""
Quality checks for persistent JARVIS memories.
"""

from __future__ import annotations


MIN_MEMORY_LENGTH = 10


LOW_VALUE_PATTERNS = (
    "the user asked",
    "the user wants an answer",
    "the user is talking to jarvis",
    "the user said hello",
)


def is_quality_memory(content: str) -> bool:
    """Return True when a memory contains useful persistent information."""

    text = content.strip().lower()

    if len(text) < MIN_MEMORY_LENGTH:
        return False

    if any(
        pattern in text
        for pattern in LOW_VALUE_PATTERNS
    ):
        return False

    return True