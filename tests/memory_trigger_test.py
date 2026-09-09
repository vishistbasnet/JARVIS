"""
Tests for lightweight memory candidate detection.
"""

from core.memory_trigger import should_consider_memory


def test_detects_preference():
    assert should_consider_memory(
        "I prefer short answers."
    )


def test_detects_project():
    assert should_consider_memory(
        "I'm working on a JARVIS project."
    )


def test_detects_explicit_memory_request():
    assert should_consider_memory(
        "Remember that I like Python."
    )


def test_detects_goal():
    assert should_consider_memory(
        "My goal is to become an AI engineer."
    )


def test_ignores_normal_question():
    assert not should_consider_memory(
        "What is the capital of France?"
    )


def test_ignores_command():
    assert not should_consider_memory(
        "Open YouTube."
    )


def test_ignores_empty_message():
    assert not should_consider_memory("")