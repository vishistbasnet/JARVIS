import pytest

from config import Settings, settings


def test_settings_load():
    """Verify that JARVIS configuration loads correctly."""
    assert settings.app_name == "JARVIS"
    assert settings.llm_provider
    assert settings.llm_model
    assert settings.stt_model_size
    assert settings.tts_engine


def test_settings_load_with_defaults(monkeypatch):
    """Settings should load safely without a .env file."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    test_settings = Settings(_env_file=None)

    assert test_settings.app_name == "JARVIS"
    assert test_settings.llm_provider == "gemini"
    assert test_settings.log_level == "INFO"


def test_require_llm_key_raises_when_missing():
    """Missing LLM API key should raise an error."""
    test_settings = Settings(
        _env_file=None,
        llm_api_key="",
    )

    with pytest.raises(
        RuntimeError,
        match="LLM_API_KEY is not set",
    ):
        test_settings.require_llm_key()


def test_require_llm_key_passes_when_present():
    """A configured LLM API key should pass validation."""
    test_settings = Settings(
        _env_file=None,
        llm_api_key="sk-test-fake-key",
    )

    test_settings.require_llm_key()


def test_invalid_log_level_rejected():
    """Invalid log levels should be rejected."""
    with pytest.raises(ValueError):
        Settings(
            _env_file=None,
            log_level="NOT_A_LEVEL",
        )


def test_log_level_case_insensitive():
    """Log levels should be normalized to uppercase."""
    test_settings = Settings(
        _env_file=None,
        log_level="debug",
    )

    assert test_settings.log_level == "DEBUG"
