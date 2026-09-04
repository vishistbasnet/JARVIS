"""
Central configuration for JARVIS.

All configuration is loaded from environment variables (typically via a
`.env` file, see `.env.example`). No secrets ever live in source code.

Why pydantic-settings instead of plain os.getenv() calls scattered around
the codebase:
  - Validation happens once, at startup, in one place. If LLM_API_KEY is
    missing, we find out immediately with a clear error instead of an
    obscure failure three tool calls deep.
  - Every other module imports a single, typed `settings` object instead
    of re-reading environment variables everywhere.
  - It's easy to extend later (new API keys, new feature flags) without
    changing the modules that consume `settings`.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DB_PATH = DATA_DIR / "memory.db"


class Settings(BaseSettings):
    """
    Application settings, populated from environment variables / `.env`.

    Field names map to environment variable names (case-insensitive).
    E.g. `llm_api_key` reads from `LLM_API_KEY`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # unrelated env vars on the machine shouldn't error
    )

    # --- LLM provider -----------------------------------------------------
    llm_provider: str = Field(
        default="gemini",
        description="LLM provider used by JARVIS.",
    )
    llm_api_key: str = Field(
        default="",
        description="API key for the configured LLM provider.",
    )
    llm_model: str = Field(
        default="gemini-3.5-flash-lite",
        description="Model used for JARVIS conversations.",
    )
    # --- Web search --------------------------------------------------------
    tavily_api_key: str = Field(
        default="",
        description="API key for Tavily web search.",
    )
    # --- Speech -------------------------------------------------------------
    stt_model_size: str = Field(
        default="base",
        description="faster-whisper model size: tiny, base, small, medium, large.",
    )
    tts_engine: str = Field(
        default="edge-tts",
        description="'edge-tts' (online, natural voice) or 'pyttsx3' "
        "(offline, robotic but always available).",
    )
    tts_voice: str = Field(
        default="en-US-GuyNeural",
        description="Voice name, used only when tts_engine is 'edge-tts'.",
    )

    # --- App behavior ---------------------------------------------------
    app_name: str = Field(default="JARVIS")
    log_level: str = Field(default="INFO")
    database_path: Path = Field(default=DEFAULT_DB_PATH)

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = value.upper()
        if upper not in valid:
            raise ValueError(f"log_level must be one of {valid}, got {value!r}")
        return upper

    def require_llm_key(self) -> None:
        """
        Raise a clear, actionable error if the LLM API key is missing.

        Called explicitly at the point features actually need the LLM
        (rather than at import time), so e.g. running unit tests for the
        calculator doesn't require an API key to be set at all.
        """
        if not self.llm_api_key:
            raise RuntimeError(
                "LLM_API_KEY is not set. Copy .env.example to .env and fill "
                "in your API key before starting JARVIS."
            )


# Singleton settings instance. Import this everywhere:
#   from config import settings
settings = Settings()