"""
LLM abstraction for JARVIS.

The rest of the application interacts with the LLMProvider interface
instead of directly depending on a specific vendor SDK.

Current implementation:
    GeminiProvider -> Google Gemini API
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from google import genai

from ai.prompts import JARVIS_SYSTEM_PROMPT
from config import settings

from utils.logger import get_logger


logger = get_logger(__name__)


class LLMProvider(ABC):
    """
    Abstract interface for an LLM provider.

    Any future provider (Claude, OpenAI, local LLM, etc.) should
    implement this interface.
    """

    @abstractmethod
    def chat(self, message: str) -> str:
        """
        Send a message to the LLM and return its text response.
        """
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation of the LLMProvider interface.
    """

    def __init__(self) -> None:
        settings.require_llm_key()

        self.client = genai.Client(
            api_key=settings.llm_api_key
        )

        self.model = settings.llm_model

        logger.info(
            "Gemini provider initialized with model: %s",
            self.model,
        )

    def chat(self, message: str) -> str:
        """
        Send a single user message to Gemini.

        Args:
            message: User's text input.

        Returns:
            Gemini's response as plain text.

        Raises:
            RuntimeError: If the Gemini API request fails.
        """

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        logger.info("Sending message to Gemini")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=message,
                config={
                    "system_instruction": JARVIS_SYSTEM_PROMPT,
                },
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            logger.info("Gemini response received.")

            return response.text.strip()

        except Exception as exc:
            logger.exception("Gemini API request failed.")

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc


def create_llm_provider() -> LLMProvider:
    """
    Create the configured LLM provider.

    Keeping provider creation here means the rest of JARVIS
    doesn't need to know which vendor is being used.
    """

    provider = settings.llm_provider.lower().strip()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider!r}"
    )