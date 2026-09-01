from config import settings


def test_settings_load():
    """Verify that JARVIS configuration loads correctly."""
    assert settings.app_name == "JARVIS"
    assert settings.llm_provider
    assert settings.llm_model
    assert settings.stt_model_size
    assert settings.tts_engine