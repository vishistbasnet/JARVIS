from core.memory_manager import MemoryManager
from core.memory_store import MemoryStore


def create_manager(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")
    return MemoryManager(store)


def test_remember_creates_memory(tmp_path):
    manager = create_manager(tmp_path)

    memory = manager.remember(
        "My preferred name is Vishist.",
        category="preference",
    )

    assert memory.memory_id is not None
    assert memory.content == "My preferred name is Vishist."
    assert memory.category == "preference"


def test_recall_returns_memory(tmp_path):
    manager = create_manager(tmp_path)

    saved = manager.remember(
        "I prefer concise answers.",
        category="preference",
    )

    memory = manager.recall(saved.memory_id)

    assert memory is not None
    assert memory.memory_id == saved.memory_id
    assert memory.content == saved.content


def test_recall_missing_memory(tmp_path):
    manager = create_manager(tmp_path)

    assert manager.recall(999) is None


def test_list_memories(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember("Memory one")
    manager.remember("Memory two", category="project")

    memories = manager.list_memories()

    assert len(memories) == 2
    assert memories[0].content == "Memory one"
    assert memories[1].content == "Memory two"


def test_forget_removes_memory(tmp_path):
    manager = create_manager(tmp_path)

    saved = manager.remember("The user wants to remember this.")

    assert saved is not None
    assert manager.forget(saved.memory_id) is True
    assert manager.recall(saved.memory_id) is None


def test_forget_missing_memory(tmp_path):
    manager = create_manager(tmp_path)

    assert manager.forget(999) is False

def test_search_returns_relevant_memories(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember(
        "I am working on the JARVIS project.",
        category="project",
    )

    manager.remember(
        "I prefer concise answers.",
        category="preference",
    )

    manager.remember(
        "My favorite color is blue.",
        category="personal",
    )

    results = manager.search("Tell me about my JARVIS project")

    assert len(results) >= 1
    assert results[0].content == (
        "I am working on the JARVIS project."
    )


def test_search_respects_limit(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember("JARVIS project one")
    manager.remember("JARVIS project two")
    manager.remember("JARVIS project three")

    results = manager.search(
        "JARVIS project",
        limit=2,
    )

    assert len(results) == 2


def test_search_empty_query_returns_empty(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember("Some memory")

    assert manager.search("") == []
    assert manager.search("   ") == []


def test_search_returns_empty_when_nothing_matches(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember("I like Python.")

    assert manager.search("quantum physics") == []

def test_build_context_returns_relevant_memories(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember(
        "I am working on the JARVIS project.",
        category="project",
    )

    manager.remember(
        "I prefer concise answers.",
        category="preference",
    )

    manager.remember(
        "My favorite color is blue.",
        category="personal",
    )

    context = manager.build_context(
        "Tell me about my JARVIS project"
    )

    assert "Relevant memories about the user:" in context
    assert (
        "[project] I am working on the JARVIS project."
        in context
    )


def test_build_context_returns_empty_when_no_match(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember(
        "I like Python.",
        category="preference",
    )

    context = manager.build_context(
        "Tell me about quantum physics"
    )

    assert context == ""


def test_build_context_respects_limit(tmp_path):
    manager = create_manager(tmp_path)

    manager.remember("JARVIS project one")
    manager.remember("JARVIS project two")
    manager.remember("JARVIS project three")

    context = manager.build_context(
        "JARVIS project",
        limit=2,
    )

    assert context.count("[general]") == 2

def test_remember_rejects_sensitive_memory(tmp_path):
    manager = create_manager(tmp_path)

    memory = manager.remember(
        "The user's API key is EXAMPLE_SECRET.",
        category="personal",
    )

    assert memory is None
    assert manager.list_memories() == []

def test_remember_allows_safe_memory(tmp_path):
    manager = create_manager(tmp_path)

    memory = manager.remember(
        "The user prefers concise answers.",
        category="preference",
    )

    assert memory is not None
    assert memory.content == (
        "The user prefers concise answers."
    )

def test_remember_rejects_low_quality_memory(tmp_path):
    manager = create_manager(tmp_path)

    memory = manager.remember(
        "Hello",
        category="general",
    )

    assert memory is None
    assert manager.list_memories() == []

def test_remember_rejects_conversation_state(tmp_path):
    manager = create_manager(tmp_path)

    memory = manager.remember(
        "The user is talking to JARVIS.",
        category="general",
    )

    assert memory is None
    assert manager.list_memories() == []

def test_memory_pipeline_rejects_unsafe_low_quality_and_duplicate(
    tmp_path,
):
    manager = create_manager(tmp_path)

    unsafe = manager.remember(
        "The user's API key is EXAMPLE_SECRET.",
        category="personal",
    )

    low_quality = manager.remember(
        "Hello",
        category="general",
    )

    first = manager.remember(
        "The user prefers concise answers.",
        category="preference",
    )

    duplicate = manager.remember(
        "THE USER PREFERS CONCISE ANSWERS.",
        category="preference",
    )

    assert unsafe is None
    assert low_quality is None
    assert first is not None
    assert duplicate is None

    stored = manager.list_memories()

    assert len(stored) == 1
    assert stored[0].category == "preference"