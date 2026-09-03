from __future__ import annotations

from ai.llm import create_llm_provider
from core.context import ContextManager
from speech.listener import SpeechListener
from speech.speaker import SpeechSpeaker
from utils.logger import get_logger


logger = get_logger(__name__)


class Assistant:
    """Main JARVIS voice assistant."""

    def __init__(self) -> None:
        logger.info("Initializing JARVIS assistant...")

        self.listener = SpeechListener()
        self.llm = create_llm_provider()
        self.speaker = SpeechSpeaker()

        # Short-term conversation memory.
        self.context = ContextManager(
            max_messages=10
        )

        logger.info(
            "JARVIS assistant initialized successfully."
        )

    def process_once(
        self,
        duration: float = 5.0,
    ) -> str:

        logger.info(
            "Waiting for user speech..."
        )

        result = self.listener.listen(
            duration=duration
        )

        user_text = result.text.strip()

        if not user_text:
            logger.warning(
                "No speech was recognized."
            )

            return ""

        logger.info(
            "User said: %s",
            user_text,
        )

        # Save user message.
        self.context.add_user_message(
            user_text
        )

        # Get complete conversation history.
        history = self.context.get_messages()

        logger.info(
            "Conversation context contains %d messages.",
            len(history),
        )

        logger.info(
            "Sending user message to LLM..."
        )

        # Send current message + conversation history.
        response = self.llm.chat(
            user_text,
            history=history[:-1],
        )

        logger.info(
            "LLM response received."
        )

        # Save JARVIS response.
        self.context.add_assistant_message(
            response
        )

        logger.info(
            "Speaking JARVIS response..."
        )

        self.speaker.speak(response)

        logger.info(
            "Voice interaction completed."
        )

        return response