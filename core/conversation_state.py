"""
Conversation state management for JARVIS.

Keeps track of the current conversational lifecycle
without mixing state logic into the Assistant class.
"""

from __future__ import annotations

from enum import Enum


class ConversationState(str, Enum):
    """Possible states of a JARVIS conversation."""

    IDLE = "idle"
    ACTIVE = "active"
    ENDED = "ended"


class ConversationStateManager:
    """Manage the current conversation state."""

    def __init__(self) -> None:
        self._state = ConversationState.IDLE

    @property
    def state(self) -> ConversationState:
        """Return the current conversation state."""

        return self._state

    def start(self) -> None:
        """Start or resume a conversation."""

        self._state = ConversationState.ACTIVE

    def end(self) -> None:
        """End the current conversation."""

        self._state = ConversationState.ENDED

    def reset(self) -> None:
        """Reset the conversation back to idle."""

        self._state = ConversationState.IDLE

    def is_active(self) -> bool:
        """Return True when the conversation is active."""

        return self._state == ConversationState.ACTIVE

    def is_ended(self) -> bool:
        """Return True when the conversation has ended."""

        return self._state == ConversationState.ENDED