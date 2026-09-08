from unittest.mock import Mock

import httpx
import pytest

from ai.llm import (
    MAX_GEMINI_ATTEMPTS,
    _generate_with_retry,
)
from core.errors import LLMError


def test_retry_succeeds_after_transient_error(monkeypatch):
    client = Mock()

    client.models.generate_content.side_effect = [
        httpx.ConnectError("temporary network failure"),
        "success",
    ]

    sleep_mock = Mock()
    monkeypatch.setattr("ai.llm.time.sleep", sleep_mock)

    result = _generate_with_retry(
        client=client,
        model="test-model",
        contents="hello",
        config={},
    )

    assert result == "success"
    assert client.models.generate_content.call_count == 2
    sleep_mock.assert_called_once_with(1.0)


def test_retry_succeeds_after_two_transient_errors(monkeypatch):
    client = Mock()

    client.models.generate_content.side_effect = [
        httpx.ConnectError("temporary failure 1"),
        httpx.ConnectError("temporary failure 2"),
        "success",
    ]

    sleep_mock = Mock()
    monkeypatch.setattr("ai.llm.time.sleep", sleep_mock)

    result = _generate_with_retry(
        client=client,
        model="test-model",
        contents="hello",
        config={},
    )

    assert result == "success"
    assert client.models.generate_content.call_count == 3
    assert sleep_mock.call_count == 2

    sleep_mock.assert_any_call(1.0)
    sleep_mock.assert_any_call(2.0)


def test_retry_fails_after_max_attempts(monkeypatch):
    client = Mock()

    client.models.generate_content.side_effect = (
        httpx.ConnectError("network unavailable")
    )

    sleep_mock = Mock()
    monkeypatch.setattr("ai.llm.time.sleep", sleep_mock)

    with pytest.raises(LLMError, match="after 3 attempts"):
        _generate_with_retry(
            client=client,
            model="test-model",
            contents="hello",
            config={},
        )

    assert (
        client.models.generate_content.call_count
        == MAX_GEMINI_ATTEMPTS
    )

    assert sleep_mock.call_count == MAX_GEMINI_ATTEMPTS - 1


def test_non_transient_error_is_not_retried(monkeypatch):
    client = Mock()

    client.models.generate_content.side_effect = ValueError(
        "invalid request"
    )

    sleep_mock = Mock()
    monkeypatch.setattr("ai.llm.time.sleep", sleep_mock)

    with pytest.raises(LLMError, match="Gemini request failed"):
        _generate_with_retry(
            client=client,
            model="test-model",
            contents="hello",
            config={},
        )

    assert client.models.generate_content.call_count == 1
    sleep_mock.assert_not_called()