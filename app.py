"""
JARVIS entry point.

At this stage (Phase 0), this file does NOT run the assistant yet — there's
no speech, no LLM, no tools implemented. Its only job right now is to prove
that the project scaffolding works end-to-end:

  1. Environment variables load correctly via config.py
  2. Logging is configured and writing to console + file
  3. The project structure imports cleanly with no circular-import issues

Phase 1 will replace the body of main() with the actual listen -> think ->
speak loop.
"""

from __future__ import annotations

import sys

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def main() -> int:
    logger.info("Starting %s (Phase 0: scaffolding check)", settings.app_name)
    logger.info("LLM provider configured: %s", settings.llm_provider)
    logger.info("LLM model configured: %s", settings.llm_model)
    logger.info("STT model size: %s", settings.stt_model_size)
    logger.info("TTS engine: %s", settings.tts_engine)
    logger.info("Database path: %s", settings.database_path)

    if not settings.llm_api_key:
        logger.warning(
            "LLM_API_KEY is not set. That's expected for Phase 0 — "
            "you'll need it starting Phase 2 (AI conversation)."
        )

    print(f"\n{settings.app_name} scaffolding is healthy.")
    print("Config loaded, logging works, project structure imports cleanly.")
    print("Nothing to talk to yet — that starts in Phase 1.\n")

    logger.info("Phase 0 startup check complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())