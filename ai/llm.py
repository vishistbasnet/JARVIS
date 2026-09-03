from __future__ import annotations

from abc import ABC, abstractmethod

from google import genai

from ai.prompts import JARVIS_SYSTEM_PROMPT
from config import settings
from core.context import Message
from utils.logger import get_logger


logger = get_logger(__name__)


class LLMProvider(ABC):
    """Base interface for LLM providers."""

    @abstractmethod
    def chat(
        self,
        message: str,
        history: list[Message] | None = None,
    ) -> str:
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Gemini implementation of the LLM provider."""

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

    def chat(
        self,
        message: str,
        history: list[Message] | None = None,
    ) -> str:

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        logger.info("Sending message to Gemini")

        contents = []

        # Add previous conversation history.
        if history:
            for item in history:
                contents.append(
                    {
                        "role": (
                            "user"
                            if item.role == "user"
                            else "model"
                        ),
                        "parts": [
                            {
                                "text": item.content
                            }
                        ],
                    }
                )

        # Add current user message.
        contents.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": message.strip()
                    }
                ],
            }
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
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
            logger.exception(
                "Gemini API request failed."
            )

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc


def create_llm_provider() -> LLMProvider:
    """Create the configured LLM provider."""

    provider = settings.llm_provider.lower().strip()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider!r}"
    )