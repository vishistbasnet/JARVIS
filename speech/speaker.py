"""
Text-to-speech speaker for JARVIS.

Uses:
    - edge-tts for speech generation
    - pygame for controlled MP3 playback
"""

from __future__ import annotations

import asyncio
import tempfile
import time
from pathlib import Path

import edge_tts
import pygame

from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


class SpeechSpeaker:
    """Convert text into speech and play it through the default speaker."""

    def __init__(
        self,
        voice: str | None = None,
    ) -> None:
        self.voice = voice or settings.tts_voice

        logger.info("TTS voice configured: %s", self.voice)

    async def _generate(
        self,
        text: str,
        output_file: Path,
    ) -> None:
        """Generate speech audio using Edge TTS."""

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
        )

        await communicate.save(str(output_file))

    @staticmethod
    def _play_audio(audio_file: Path) -> None:
        """
        Play an MP3 file and wait until playback finishes.
        """

        logger.info("Playing audio: %s", audio_file.name)

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.

        Args:
            text: Text JARVIS should speak.
        """

        if not text or not text.strip():
            logger.warning("Empty text received. Nothing to speak.")
            return

        text = text.strip()

        logger.info("Speaking: %s", text)

        output_file: Path | None = None

        try:
            # Create a temporary MP3 file.
            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False,
            ) as temp:
                output_file = Path(temp.name)

            # Generate speech.
            asyncio.run(
                self._generate(
                    text,
                    output_file,
                )
            )

            logger.info("Speech audio generated successfully.")

            # Play and WAIT until playback is complete.
            self._play_audio(output_file)

            logger.info("Speech playback completed.")

        except Exception as exc:
            logger.exception("Text-to-speech failed.")

            raise RuntimeError(
                f"Could not generate or play speech: {exc}"
            ) from exc

        finally:
            # Delete the temporary MP3 only AFTER playback.
            if output_file and output_file.exists():
                try:
                    output_file.unlink()
                    logger.debug(
                        "Temporary audio file deleted: %s",
                        output_file.name,
                    )
                except OSError:
                    logger.warning(
                        "Could not delete temporary audio file: %s",
                        output_file,
                    )