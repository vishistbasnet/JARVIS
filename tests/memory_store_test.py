from datetime import datetime

from core.memory import Memory
from core.memory_store import MemoryStore


def test_memory_store_creates_database(tmp_path):
    database_path = tmp_path / "memory.db"

    store = MemoryStore(database_path)

    assert database_path.exists()
    assert store.get_all() == []


def test_memory_store_adds_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    memory = Memory(
        content="My preferred name is Vishist.",
        category="preference",
    )

    saved = store.add(memory)

    assert saved.memory_id is not None
    assert saved.content == memory.content
    assert saved.category == "preference"
    assert isinstance(saved.created_at, datetime)
    assert isinstance(saved.updated_at, datetime)


def test_memory_store_gets_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    saved = store.add(
        Memory(
            content="I prefer concise answers.",
            category="preference",
        )
    )

    retrieved = store.get(saved.memory_id)

    assert retrieved is not None
    assert retrieved.memory_id == saved.memory_id
    assert retrieved.content == saved.content
    assert retrieved.category == saved.category


def test_memory_store_returns_none_for_missing_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    assert store.get(999) is None


def test_memory_store_get_all(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    store.add(
        Memory(
            content="Memory one",
            category="general",
        )
    )

    store.add(
        Memory(
            content="Memory two",
            category="project",
        )
    )

    memories = store.get_all()

    assert len(memories) == 2
    assert memories[0].content == "Memory one"
    assert memories[1].content == "Memory two"


def test_memory_store_deletes_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    saved = store.add(
        Memory(
            content="Temporary memory",
            category="general",
        )
    )

    assert store.delete(saved.memory_id) is True
    assert store.get(saved.memory_id) is None


def test_memory_store_delete_missing_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    assert store.delete(999) is False


def test_memory_persists_across_store_instances(tmp_path):
    database_path = tmp_path / "memory.db"

    first_store = MemoryStore(database_path)

    saved = first_store.add(
        Memory(
            content="This should survive a restart.",
            category="project",
        )
    )

    second_store = MemoryStore(database_path)

    retrieved = second_store.get(saved.memory_id)

    assert retrieved is not None
    assert retrieved.content == "This should survive a restart."
    assert retrieved.category == "project"