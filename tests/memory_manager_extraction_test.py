"""
Tests for memory extraction and persistence integration.
"""

from unittest.mock import MagicMock

from core.memory import Memory
from core.memory_manager import MemoryManager
from core.memory_store import MemoryStore


def create_manager(tmp_path):
    store = MemoryStore(
        tmp_path / "memory.db"
    )

    return MemoryManager(store=store)


def test_remember_from_message_persists_extracted_memory(tmp_path):
    manager = create_manager(tmp_path)

    extractor = MagicMock()

    extractor.extract.return_value = Memory(
        content="The user prefers concise answers.",
        category="preference",
    )

    memory = manager.remember_from_message(
        "I prefer concise answers.",
        extractor,
    )

    assert memory is not None
    assert memory.memory_id is not None
    assert memory.content == (
        "The user prefers concise answers."
    )
    assert memory.category == "preference"

    stored = manager.list_memories()

    assert len(stored) == 1
    assert stored[0].content == (
        "The user prefers concise answers."
    )


def test_remember_from_message_does_not_persist_when_no_memory(
    tmp_path,
):
    manager = create_manager(tmp_path)

    extractor = MagicMock()
    extractor.extract.return_value = None

    memory = manager.remember_from_message(
        "What is the capital of France?",
        extractor,
    )

    assert memory is None
    assert manager.list_memories() == []

    extractor.extract.assert_called_once_with(
        "What is the capital of France?"
    )

def test_remember_from_message_does_not_store_duplicate(
    tmp_path,
):
    manager = create_manager(tmp_path)

    extractor = MagicMock()

    extractor.extract.return_value = Memory(
        content="The user prefers concise answers.",
        category="preference",
    )

    first = manager.remember_from_message(
        "I prefer concise answers.",
        extractor,
    )

    second = manager.remember_from_message(
        "I prefer concise answers.",
        extractor,
    )

    assert first is not None
    assert second is None

    stored = manager.list_memories()

    assert len(stored) == 1
    assert stored[0].content == (
        "The user prefers concise answers."
    )

def test_remember_from_message_rejects_sensitive_extracted_memory(
    tmp_path,
):
    manager = create_manager(tmp_path)

    extractor = MagicMock()

    extractor.extract.return_value = Memory(
        content="The user's API key is EXAMPLE_SECRET.",
        category="personal",
    )

    memory = manager.remember_from_message(
        "Remember my API key.",
        extractor,
    )

    assert memory is None
    assert manager.list_memories() == []

def test_remember_from_message_rejects_password_memory(
    tmp_path,
):
    manager = create_manager(tmp_path)

    extractor = MagicMock()

    extractor.extract.return_value = Memory(
        content="The user's password is secret123.",
        category="personal",
    )

    memory = manager.remember_from_message(
        "Remember my password.",
        extractor,
    )

    assert memory is None
    assert manager.list_memories() == []