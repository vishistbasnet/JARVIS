"""
Lightweight local detection for potential user memories.
"""

from __future__ import annotations


MEMORY_PATTERNS = (
    "remember that",
    "remember this",
    "i prefer",
    "i like",
    "i love",
    "i hate",
    "i don't like",
    "i am working on",
    "i'm working on",
    "i work on",
    "my goal is",
    "i want to learn",
    "i want to become",
    "my favorite",
)


def should_consider_memory(message: str) -> bool:
    """Return True when a message may contain useful user memory."""

    text = message.strip().lower()

    if not text:
        return False

    return any(
        pattern in text
        for pattern in MEMORY_PATTERNS
    )