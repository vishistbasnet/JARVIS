from unittest.mock import Mock

import numpy as np
import pytest

from core.assistant import Assistant
from core.errors import SpeechError
from speech.listener import SpeechListener


def test_record_microphone_failure_raises_speech_error(monkeypatch):
    listener = SpeechListener()

    def failing_record(*args, **kwargs):
        raise RuntimeError("Microphone unavailable")

    monkeypatch.setattr(
        "speech.listener.sd.rec",
        failing_record,
    )

    with pytest.raises(
        SpeechError,
        match="Could not record from the microphone",
    ):
        listener.record(duration=1.0)


def test_transcribe_failure_raises_speech_error():
    listener = SpeechListener()

    listener._model = Mock()

    listener._model.transcribe.side_effect = RuntimeError(
        "Whisper failed"
    )

    audio = np.zeros(16000, dtype=np.float32)

    with pytest.raises(
        SpeechError,
        match="Could not transcribe audio",
    ):
        listener.transcribe(audio)


def test_process_once_handles_speech_error():
    assistant = Assistant.__new__(Assistant)

    assistant.listener = Mock()

    assistant.listener.listen.side_effect = SpeechError(
        "Microphone unavailable"
    )

    result = assistant.process_once()

    assert result == ""

    assistant.listener.listen.assert_called_once_with(
        duration=5.0
    )


def test_process_once_passes_custom_duration():
    assistant = Assistant.__new__(Assistant)

    assistant.listener = Mock()

    assistant.listener.listen.side_effect = SpeechError(
        "Speech recognition failed"
    )

    result = assistant.process_once(duration=3.0)

    assert result == ""

    assistant.listener.listen.assert_called_once_with(
        duration=3.0
    )