"""
Safety manager for JARVIS.

Handles confirmation requirements for potentially dangerous actions.
"""

from __future__ import annotations

from typing import Any


class SafetyManager:
    """Manage confirmation requirements for sensitive actions."""

    CONFIRMATION_REQUIRED_ACTIONS = {
        "shutdown",
        "restart",
    }

    CONFIRMATION_WORDS = {
        "yes",
        "yeah",
        "yep",
        "sure",
        "confirm",
        "confirmed",
        "do it",
        "go ahead",
        "yes i want to shut it down"
    }

    CANCELLATION_WORDS = {
        "no",
        "nope",
        "cancel",
        "stop",
        "don't",
        "do not",
        "no i don't"
    }

    @classmethod
    def requires_confirmation(cls, action: str) -> bool:
        """Return whether an action requires confirmation."""

        action = action.strip().lower()

        return action in cls.CONFIRMATION_REQUIRED_ACTIONS

    @classmethod
    def is_confirmation(cls, response: str) -> bool:
        """Return whether a response confirms the requested action."""

        response = response.strip().lower()

        return response in cls.CONFIRMATION_WORDS

    @classmethod
    def is_cancellation(cls, response: str) -> bool:
        """Return whether a response cancels the requested action."""

        response = response.strip().lower()

        return response in cls.CANCELLATION_WORDS

    @classmethod
    def check_action(
        cls,
        action: str,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """
        Determine whether an action can proceed.

        Dangerous actions require explicit confirmation.
        """

        action = action.strip().lower()

        if not action:
            raise ValueError("Action cannot be empty.")

        if not cls.requires_confirmation(action):
            return {
                "status": "allowed",
                "action": action,
                "requires_confirmation": False,
            }

        if confirm:
            return {
                "status": "allowed",
                "action": action,
                "requires_confirmation": True,
            }

        return {
            "status": "confirmation_required",
            "action": action,
            "requires_confirmation": True,
            "message": (
                f"Confirmation is required before {action}."
            ),
        }