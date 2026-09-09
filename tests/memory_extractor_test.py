"""
Tests for automatic memory extraction.
"""

from unittest.mock import MagicMock

from core.memory_extractor import MemoryExtractor


def test_extracts_memory_from_llm_response():
    llm = MagicMock()

    llm.chat.return_value = """
{
    "should_remember": true,
    "content": "The user prefers concise answers.",
    "category": "preference"
}
"""

    extractor = MemoryExtractor(llm)

    memory = extractor.extract(
        "I prefer concise answers."
    )

    assert memory is not None
    assert memory.content == (
        "The user prefers concise answers."
    )
    assert memory.category == "preference"


def test_returns_none_when_llm_says_not_to_remember():
    llm = MagicMock()

    llm.chat.return_value = """
{
    "should_remember": false,
    "content": "",
    "category": "general"
}
"""

    extractor = MemoryExtractor(llm)

    memory = extractor.extract(
        "What is the capital of France?"
    )

    assert memory is None


def test_returns_none_for_invalid_json():
    llm = MagicMock()

    llm.chat.return_value = "This is not valid JSON."

    extractor = MemoryExtractor(llm)

    memory = extractor.extract(
        "I like Python."
    )

    assert memory is None


def test_returns_none_for_empty_message():
    llm = MagicMock()

    extractor = MemoryExtractor(llm)

    memory = extractor.extract("   ")

    assert memory is None

    llm.chat.assert_not_called()


def test_invalid_category_falls_back_to_general():
    llm = MagicMock()

    llm.chat.return_value = """
{
    "should_remember": true,
    "content": "The user likes Python.",
    "category": "unknown"
}
"""

    extractor = MemoryExtractor(llm)

    memory = extractor.extract(
        "I really like Python."
    )

    assert memory is not None
    assert memory.content == "The user likes Python."
    assert memory.category == "general"