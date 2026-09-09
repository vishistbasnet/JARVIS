from types import SimpleNamespace
from unittest.mock import Mock

from core.assistant import Assistant
from core.errors import SpeechError


def test_confirmation_speech_error_does_not_crash():
    assistant = Assistant()

    assistant.speaker = Mock()
    assistant.speaker.speak = Mock()

    assistant.listener = Mock()
    assistant.listener.listen.side_effect = SpeechError(
        "Microphone unavailable"
    )

    function_call = SimpleNamespace(
        args={
            "action": "shutdown",
        }
    )

    result = assistant._handle_confirmation(
        function_call,
        5.0,
    )

    assert result is False

    assistant.speaker.speak.assert_called()