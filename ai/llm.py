"""
LLM providers for JARVIS.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import time
from typing import Any

import httpx
from google import genai
from google.genai import errors

from ai.prompts import JARVIS_SYSTEM_PROMPT
from config import settings
from core.context import Message
from core.errors import LLMError
from utils.logger import get_logger


logger = get_logger(__name__)


MAX_GEMINI_ATTEMPTS = 3
RETRY_DELAYS = (1.0, 2.0)


def _is_transient_gemini_error(exc: Exception) -> bool:
    """
    Determine whether a Gemini failure is likely temporary.

    Only transient network/server/rate-limit failures should be retried.
    """

    if isinstance(
        exc,
        (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.ReadTimeout,
            httpx.WriteTimeout,
            httpx.NetworkError,
        ),
    ):
        return True

    if isinstance(exc, errors.ServerError):
        return True

    if isinstance(exc, errors.APIError):
        status_code = getattr(exc, "status_code", None)

        return status_code in {
            429,  # Too Many Requests
            500,
            502,
            503,
            504,
        }

    return False


def _generate_with_retry(
    client: Any,
    model: str,
    contents: Any,
    config: Any,
) -> Any:
    """
    Generate Gemini content with bounded retry handling.

    This helper is only for Gemini API calls.
    It must never be used around tool execution.
    """

    last_error: Exception | None = None

    for attempt in range(1, MAX_GEMINI_ATTEMPTS + 1):
        try:
            logger.info(
                "Gemini request attempt %d/%d",
                attempt,
                MAX_GEMINI_ATTEMPTS,
            )

            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

        except Exception as exc:
            last_error = exc

            if not _is_transient_gemini_error(exc):
                logger.exception(
                    "Non-transient Gemini error."
                )
                raise LLMError(
                    f"Gemini request failed: {exc}"
                ) from exc

            if attempt >= MAX_GEMINI_ATTEMPTS:
                logger.exception(
                    "Gemini request failed after %d attempts.",
                    MAX_GEMINI_ATTEMPTS,
                )

                raise LLMError(
                    "Gemini request failed after "
                    f"{MAX_GEMINI_ATTEMPTS} attempts: {exc}"
                ) from exc

            delay = RETRY_DELAYS[attempt - 1]

            logger.warning(
                "Transient Gemini error on attempt %d/%d: %s. "
                "Retrying in %.1f seconds.",
                attempt,
                MAX_GEMINI_ATTEMPTS,
                exc,
                delay,
            )

            time.sleep(delay)

    raise LLMError(
        f"Gemini request failed: {last_error}"
    )


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

        response = _generate_with_retry(
            client=self.client,
            model=self.model,
            contents=contents,
            config={
                "system_instruction": JARVIS_SYSTEM_PROMPT,
            },
        )

        if not response.text:
            raise LLMError(
                "Gemini returned an empty response."
            )

        logger.info("Gemini response received.")

        return response.text.strip()


def create_llm_provider() -> LLMProvider:
    """Create the configured LLM provider."""

    provider = settings.llm_provider.lower().strip()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider!r}"
    )