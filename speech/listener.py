"""
Speech-to-text listener for JARVIS.

Uses:
    - sounddevice for microphone recording
    - faster-whisper for speech recognition

This module is intentionally independent from the AI/LLM layer.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

from config import settings
from core.errors import SpeechError
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SpeechResult:
    """Result returned after speech recognition."""

    text: str
    duration: float


class SpeechListener:
    """
    Records audio from the default microphone and transcribes it
    using faster-whisper.
    """

    SAMPLE_RATE = 16_000
    CHANNELS = 1
    DTYPE = "float32"

    def __init__(
        self,
        model_size: str | None = None,
    ) -> None:
        self.model_size = model_size or settings.stt_model_size
        self._model: WhisperModel | None = None

    def load_model(self) -> None:
        """Load the Whisper model into memory."""

        if self._model is not None:
            return

        logger.info(
            "Loading Whisper model: %s",
            self.model_size,
        )

        self._model = WhisperModel(
            self.model_size,
            device="cpu",
            compute_type="int8",
        )

        logger.info("Whisper model loaded successfully.")

    def record(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio from the default microphone.

        Args:
            duration: Recording duration in seconds.

        Returns:
            NumPy array containing mono float32 audio.
        """

        if duration <= 0:
            raise ValueError("Recording duration must be greater than 0.")

        logger.info("Recording for %.1f seconds...", duration)

        try:
            audio = sd.rec(
                int(duration * self.SAMPLE_RATE),
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype=self.DTYPE,
            )

            sd.wait()

        except Exception as exc:
            logger.exception("Microphone recording failed.")
            raise SpeechError(
                f"Could not record from the microphone: {exc}"
            ) from exc

        # Convert from shape (samples, 1) to (samples,)
        return np.squeeze(audio)

    def transcribe(self, audio: np.ndarray) -> str:
        """
        Convert recorded audio into text.

        Args:
            audio: Mono float32 audio samples.

        Returns:
            Recognized text.
        """

        if audio.size == 0:
            return ""

        self.load_model()

        assert self._model is not None

        logger.info("Transcribing audio...")

        try:
            segments, _info = self._model.transcribe(
                audio,
                language="en",
                beam_size=5,
                vad_filter=True,
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            ).strip()

        except Exception as exc:
            logger.exception("Speech transcription failed.")
            raise SpeechError(
                f"Could not transcribe audio: {exc}"
            ) from exc

        logger.info("Transcription complete: %s", text)

        return text

    def listen(self, duration: float = 5.0) -> SpeechResult:
        """
        Record and transcribe speech.

        This is the main method other parts of JARVIS will use later.
        """

        audio = self.record(duration)

        text = self.transcribe(audio)

        return SpeechResult(
            text=text,
            duration=duration,
        )