"""
Core orchestration layer for JARVIS.

The Assistant coordinates the three major components:

    SpeechListener -> LLMProvider -> SpeechSpeaker

It does not contain implementation details for speech recognition,
LLM communication, or text-to-speech.
"""

from __future__ import annotations

from ai.llm import create_llm_provider
from speech.listener import SpeechListener
from speech.speaker import SpeechSpeaker
from utils.logger import get_logger


logger = get_logger(__name__)


class Assistant:
    """
    Orchestrates the JARVIS voice-assistant pipeline.

    Responsibilities:
        1. Listen to the user.
        2. Send recognized text to the LLM.
        3. Speak the LLM response.
    """

    def __init__(self) -> None:
        logger.info("Initializing JARVIS assistant...")

        self.listener = SpeechListener()
        self.llm = create_llm_provider()
        self.speaker = SpeechSpeaker()

        logger.info("JARVIS assistant initialized successfully.")

    def process_once(self, duration: float = 5.0) -> str:
        """
        Process one complete voice interaction.

        Pipeline:

            Microphone
                ↓
            Speech-to-Text
                ↓
            Gemini
                ↓
            Text-to-Speech
                ↓
            Speaker

        Args:
            duration: Maximum recording duration in seconds.

        Returns:
            JARVIS's textual response.
        """

        # ----------------------------------------------------------
        # 1. LISTEN
        # ----------------------------------------------------------

        logger.info("Waiting for user speech...")

        result = self.listener.listen(duration=duration)

        user_text = result.text.strip()

        if not user_text:
            logger.warning("No speech was recognized.")
            return ""

        logger.info("User said: %s", user_text)

        # ----------------------------------------------------------
        # 2. THINK
        # ----------------------------------------------------------

        logger.info("Sending user message to LLM...")

        response = self.llm.chat(user_text)

        logger.info("LLM response received.")

        # ----------------------------------------------------------
        # 3. SPEAK
        # ----------------------------------------------------------

        logger.info("Speaking JARVIS response...")

        self.speaker.speak(response)

        logger.info("Voice interaction completed.")

        return response