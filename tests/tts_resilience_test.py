from unittest.mock import Mock

from core.assistant import Assistant


def create_assistant_for_test():
    assistant = Assistant.__new__(Assistant)

    assistant.speaker = Mock()

    return assistant


def test_speak_safely_calls_speaker():
    assistant = create_assistant_for_test()

    assistant._speak_safely("Hello Vishist.")

    assistant.speaker.speak.assert_called_once_with(
        "Hello Vishist."
    )


def test_speak_safely_survives_tts_failure(capsys):
    assistant = create_assistant_for_test()

    assistant.speaker.speak.side_effect = RuntimeError(
        "TTS service unavailable"
    )

    assistant._speak_safely("Hello Vishist.")

    captured = capsys.readouterr()

    assert "JARVIS: Hello Vishist." in captured.out
    assert "TTS unavailable: TTS service unavailable" in captured.out


def test_speak_safely_does_not_raise_tts_exception():
    assistant = create_assistant_for_test()

    assistant.speaker.speak.side_effect = RuntimeError(
        "Audio playback failed"
    )

    assistant._speak_safely(
        "This response should still be returned."
    )


def test_speak_safely_handles_unexpected_tts_exception(
    capsys,
):
    assistant = create_assistant_for_test()

    assistant.speaker.speak.side_effect = Exception(
        "Unexpected audio failure"
    )

    assistant._speak_safely("Fallback response.")

    captured = capsys.readouterr()

    assert "JARVIS: Fallback response." in captured.out
    assert (
        "TTS unavailable: Unexpected audio failure"
        in captured.out
    )