"""
Conversation context management for JARVIS.

This module manages short-term conversation history in memory.

Persistent memory will be introduced in a later module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Role = Literal["user", "assistant"]


@dataclass
class Message:
    """Represents one message in the conversation."""

    role: Role
    content: str


class ContextManager:
    """
    Manage JARVIS's short-term conversation history.

    The context exists only for the lifetime of the application process.
    """

    def __init__(self, max_messages: int = 10) -> None:
        if max_messages <= 0:
            raise ValueError("max_messages must be greater than 0.")

        self.max_messages = max_messages
        self._messages: list[Message] = []

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation."""

        content = content.strip()

        if not content:
            raise ValueError("Message content cannot be empty.")

        self._messages.append(
            Message(
                role="user",
                content=content,
            )
        )

        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Add a JARVIS response to the conversation."""

        content = content.strip()

        if not content:
            raise ValueError("Message content cannot be empty.")

        self._messages.append(
            Message(
                role="assistant",
                content=content,
            )
        )

        self._trim()

    def get_messages(self) -> list[Message]:
        """Return a copy of the conversation history."""

        return list(self._messages)

    def clear(self) -> None:
        """Clear the entire conversation history."""

        self._messages.clear()

    def count(self) -> int:
        """Return the number of stored messages."""

        return len(self._messages)

    def _trim(self) -> None:
        """
        Keep conversation within the configured limit.

        JARVIS tries to preserve complete user/assistant turns instead
        of leaving an assistant response without its corresponding user
        message at the beginning of the context.
        """

        if len(self._messages) <= self.max_messages:
            return

        self._messages = self._messages[-self.max_messages:]

        # Avoid starting the context with an orphaned assistant message.
        if self._messages and self._messages[0].role == "assistant":
            self._messages.pop(0)