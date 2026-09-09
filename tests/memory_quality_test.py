"""
Tests for memory quality filtering.
"""

from core.memory_quality import is_quality_memory


def test_allows_useful_memory():
    assert is_quality_memory(
        "The user prefers concise answers."
    )


def test_allows_project_memory():
    assert is_quality_memory(
        "The user is building a JARVIS assistant."
    )


def test_rejects_empty_memory():
    assert not is_quality_memory("")


def test_rejects_very_short_memory():
    assert not is_quality_memory("Hello")


def test_rejects_low_value_memory():
    assert not is_quality_memory(
        "The user asked a question."
    )


def test_rejects_conversation_state():
    assert not is_quality_memory(
        "The user is talking to JARVIS."
    )