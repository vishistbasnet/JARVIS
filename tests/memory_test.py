from datetime import datetime

from core.memory import Memory


def test_memory_defaults():
    memory = Memory(content="My preferred name is Vishist.")

    assert memory.content == "My preferred name is Vishist."
    assert memory.category == "general"
    assert memory.created_at is None
    assert memory.updated_at is None
    assert memory.memory_id is None


def test_memory_accepts_metadata():
    now = datetime.now()

    memory = Memory(
        content="I prefer concise answers.",
        category="preference",
        created_at=now,
        updated_at=now,
        memory_id=1,
    )

    assert memory.content == "I prefer concise answers."
    assert memory.category == "preference"
    assert memory.created_at == now
    assert memory.updated_at == now
    assert memory.memory_id == 1