"""
High-level memory management for JARVIS.
"""

from __future__ import annotations

from core.memory import Memory
from core.memory_store import MemoryStore
from core.memory_safety import is_safe_memory
from core.memory_quality import is_quality_memory

class MemoryManager:
    """Provide a high-level interface for persistent memories."""

    def __init__(self, store: MemoryStore | None = None):
        self.store = store or MemoryStore()

    def remember(
        self,
        content: str,
        category: str = "general",
    ) -> Memory | None:
        """Create and persist a safe, non-duplicate memory."""

        content = content.strip()

        if not content:
            return None

        if not is_safe_memory(content):
            return None

        if not is_quality_memory(content):
            return None

        if self._is_duplicate(
            content=content,
            category=category,
        ):
            return None

        memory = Memory(
            content=content,
            category=category,
        )

        return self.store.add(memory)

    def recall(self, memory_id: int) -> Memory | None:
        """Retrieve a memory by ID."""

        return self.store.get(memory_id)

    def list_memories(self) -> list[Memory]:
        """Return all stored memories."""

        return self.store.get_all()

    def forget(self, memory_id: int) -> bool:
        """Delete a memory by ID."""

        return self.store.delete(memory_id)

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Memory]:
        """Return memories ranked by simple token overlap."""

        if not query.strip():
            return []

        memories = self.store.get_all()

        query_words = {
            word.lower().strip(".,!?;:\"'()[]{}")
            for word in query.split()
            if word.strip(".,!?;:\"'()[]{}")
        }

        if not query_words:
            return []

        scored_memories = []

        for memory in memories:
            memory_words = {
                word.lower().strip(".,!?;:\"'()[]{}")
                for word in memory.content.split()
                if word.strip(".,!?;:\"'()[]{}")
            }

            score = len(query_words & memory_words)

            if score > 0:
                scored_memories.append((score, memory))

        scored_memories.sort(
            key=lambda item: (
                -item[0],
                item[1].memory_id or 0,
            )
        )

        return [
            memory
            for _, memory in scored_memories[:limit]
        ]

    def build_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Build a formatted context string from relevant memories."""

        memories = self.search(
            query=query,
            limit=limit,
        )

        if not memories:
            return ""

        lines = [
            "Relevant memories about the user:"
        ]

        for memory in memories:
            lines.append(
                f"- [{memory.category}] {memory.content}"
            )

        return "\n".join(lines)

    def remember_from_message(
        self,
        user_message: str,
        extractor,
    ) -> Memory | None:
        """Extract and persist a memory from a user message."""

        memory = extractor.extract(user_message)

        if memory is None:
            return None

        return self.remember(
            content=memory.content,
            category=memory.category,
        )

    def _is_duplicate(
        self,
        content: str,
        category: str,
    ) -> bool:
        """Return True when an equivalent memory already exists."""

        normalized_content = content.strip().lower()

        for memory in self.store.get_all():
            if (
                memory.category == category
                and memory.content.strip().lower()
                == normalized_content
            ):
                return True

        return False