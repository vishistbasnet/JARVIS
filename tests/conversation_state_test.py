from core.conversation_state import (
    ConversationState,
    ConversationStateManager,
)


def test_initial_state_is_idle():
    manager = ConversationStateManager()

    assert manager.state == ConversationState.IDLE
    assert manager.is_active() is False
    assert manager.is_ended() is False


def test_start_activates_conversation():
    manager = ConversationStateManager()

    manager.start()

    assert manager.state == ConversationState.ACTIVE
    assert manager.is_active() is True
    assert manager.is_ended() is False


def test_end_ends_conversation():
    manager = ConversationStateManager()

    manager.start()
    manager.end()

    assert manager.state == ConversationState.ENDED
    assert manager.is_active() is False
    assert manager.is_ended() is True


def test_reset_returns_to_idle():
    manager = ConversationStateManager()

    manager.start()
    manager.end()
    manager.reset()

    assert manager.state == ConversationState.IDLE
    assert manager.is_active() is False
    assert manager.is_ended() is False


def test_start_can_resume_ended_conversation():
    manager = ConversationStateManager()

    manager.start()
    manager.end()
    manager.start()

    assert manager.state == ConversationState.ACTIVE
    assert manager.is_active() is True


def test_state_values_are_stable():
    assert ConversationState.IDLE.value == "idle"
    assert ConversationState.ACTIVE.value == "active"
    assert ConversationState.ENDED.value == "ended"

from unittest.mock import MagicMock

from core.assistant import Assistant
from core.conversation_state import ConversationState


def test_assistant_starts_conversation_when_processing():
    assistant = Assistant.__new__(Assistant)

    assistant.conversation_state = MagicMock()
    assistant.listener = MagicMock()

    assistant.listener.listen.side_effect = Exception(
        "Stop after verifying conversation start"
    )

    try:
        assistant.process_once()
    except Exception as exc:
        assert str(exc) == "Stop after verifying conversation start"

    assistant.conversation_state.start.assert_called_once()