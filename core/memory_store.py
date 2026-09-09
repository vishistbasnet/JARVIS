"""
Persistent SQLite storage for JARVIS memories.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from core.memory import Memory


class MemoryStore:
    """Store and retrieve JARVIS memories using SQLite."""

    def __init__(self, database_path: str | Path = "data/memory.db"):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        """Create a connection to the memory database."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        return connection

    def _initialize_database(self) -> None:
        """Create the memories table if it does not already exist."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'general',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def add(self, memory: Memory) -> Memory:
        """Persist a memory and return it with its database ID."""

        now = datetime.now()

        created_at = memory.created_at or now
        updated_at = memory.updated_at or now

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories (
                    content,
                    category,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    memory.content,
                    memory.category,
                    created_at.isoformat(),
                    updated_at.isoformat(),
                ),
            )

            memory_id = cursor.lastrowid
            connection.commit()

        return Memory(
            content=memory.content,
            category=memory.category,
            created_at=created_at,
            updated_at=updated_at,
            memory_id=memory_id,
        )

    def get_all(self) -> list[Memory]:
        """Return all stored memories."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    memory_id,
                    content,
                    category,
                    created_at,
                    updated_at
                FROM memories
                ORDER BY memory_id ASC
                """
            ).fetchall()

        return [
            Memory(
                memory_id=row["memory_id"],
                content=row["content"],
                category=row["category"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )
            for row in rows
        ]

    def get(self, memory_id: int) -> Memory | None:
        """Return one memory by ID."""

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    memory_id,
                    content,
                    category,
                    created_at,
                    updated_at
                FROM memories
                WHERE memory_id = ?
                """,
                (memory_id,),
            ).fetchone()

        if row is None:
            return None

        return Memory(
            memory_id=row["memory_id"],
            content=row["content"],
            category=row["category"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def delete(self, memory_id: int) -> bool:
        """Delete a memory by ID.

        Returns True when a memory was deleted, otherwise False.
        """

        with self._connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM memories
                WHERE memory_id = ?
                """,
                (memory_id,),
            )

            connection.commit()

        return cursor.rowcount > 0