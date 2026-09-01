"""
Phase 0 tests: verify configuration loads with safe defaults and validates
correctly, without requiring a real .env file or real API keys.
"""

from __future__ import annotations

import pytest

from config import Settings


def test_settings_load_with_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """With no .env and no env vars set, Settings should still construct
    successfully using its documented defaults (no required fields)."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    settings = Settings(_env_file=None)  # ignore any real .env on disk

    assert settings.app_name == "JARVIS"
    assert settings.llm_provider == "anthropic"
    assert settings.log_level == "INFO"


def test_require_llm_key_raises_when_missing() -> None:
    settings = Settings(_env_file=None, llm_api_key="")
    with pytest.raises(RuntimeError, match="LLM_API_KEY is not set"):
        settings.require_llm_key()


def test_require_llm_key_passes_when_present() -> None:
    settings = Settings(_env_file=None, llm_api_key="sk-test-fake-key")
    settings.require_llm_key()  # should not raise


def test_invalid_log_level_rejected() -> None:
    with pytest.raises(ValueError):
        Settings(_env_file=None, log_level="NOT_A_LEVEL")


def test_log_level_case_insensitive() -> None:
    settings = Settings(_env_file=None, log_level="debug")
    assert settings.log_level == "DEBUG"