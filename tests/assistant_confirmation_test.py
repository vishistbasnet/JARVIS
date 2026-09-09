from unittest.mock import Mock

from core.assistant import Assistant


def test_confirm_planned_action_returns_true_when_confirmed():
    assistant = Assistant.__new__(Assistant)

    assistant.confirmation = Mock()
    assistant.listener = Mock()

    assistant.confirmation.request_confirmation.return_value = (
        "shutdown requires confirmation. Should I continue?"
    )
    assistant.listener.listen.return_value = "yes"
    assistant.confirmation.process_response.return_value = "confirmed"

    assistant._speak_safely = Mock()

    result = assistant._confirm_planned_action("shutdown")

    assert result is True

    assistant.confirmation.request_confirmation.assert_called_once_with(
        "shutdown"
    )
    assistant.confirmation.process_response.assert_called_once_with(
        "yes"
    )


def test_confirm_planned_action_returns_false_when_cancelled():
    assistant = Assistant.__new__(Assistant)

    assistant.confirmation = Mock()
    assistant.listener = Mock()

    assistant.confirmation.request_confirmation.return_value = (
        "shutdown requires confirmation. Should I continue?"
    )
    assistant.listener.listen.return_value = "no"
    assistant.confirmation.process_response.return_value = "cancelled"

    assistant._speak_safely = Mock()

    result = assistant._confirm_planned_action("shutdown")

    assert result is False


def test_confirm_planned_action_handles_listen_failure():
    assistant = Assistant.__new__(Assistant)

    assistant.confirmation = Mock()
    assistant.listener = Mock()

    assistant.confirmation.request_confirmation.return_value = (
        "shutdown requires confirmation. Should I continue?"
    )
    assistant.listener.listen.side_effect = RuntimeError(
        "Microphone failure"
    )

    assistant._speak_safely = Mock()

    result = assistant._confirm_planned_action("shutdown")

    assert result is False
    assistant.confirmation.cancel.assert_called_once()