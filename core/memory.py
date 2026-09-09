"""
Memory models for JARVIS.

Defines the structure used to represent persistent user memories.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Memory:
    """A single persistent memory belonging to the user."""

    content: str
    category: str = "general"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    memory_id: int | None = None