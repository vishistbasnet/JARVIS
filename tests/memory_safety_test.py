"""
Tests for memory safety filtering.
"""

from core.memory_safety import is_safe_memory


def test_allows_normal_memory():
    assert is_safe_memory(
        "The user prefers concise answers."
    )


def test_allows_project_memory():
    assert is_safe_memory(
        "The user is working on a JARVIS project."
    )


def test_rejects_api_key():
    assert not is_safe_memory(
        "The user's API key is EXAMPLE_SECRET."
    )


def test_rejects_password():
    assert not is_safe_memory(
        "The user's password is secret123."
    )


def test_rejects_access_token():
    assert not is_safe_memory(
        "The user's access token is abc123."
    )


def test_rejects_private_key():
    assert not is_safe_memory(
        "The user's private key is xyz."
    )


def test_rejects_empty_content():
    assert not is_safe_memory("")