"""
Voice confirmation manager for JARVIS.

Handles user confirmation for sensitive actions.
"""

from __future__ import annotations

from core.safety import SafetyManager


class ConfirmationManager:
    """Manage confirmation requests for sensitive actions."""

    def __init__(self) -> None:
        self._pending_action: str | None = None

    @property
    def pending_action(self) -> str | None:
        """Return the action currently waiting for confirmation."""

        return self._pending_action

    def request_confirmation(self, action: str) -> str:
        """
        Create a confirmation request for an action.
        """

        action = action.strip().lower()

        if not action:
            raise ValueError("Action cannot be empty.")

        if not SafetyManager.requires_confirmation(action):
            raise ValueError(
                f"Action does not require confirmation: {action}"
            )

        self._pending_action = action

        return (
            f"{action.capitalize()} requires confirmation. "
            "Should I continue?"
        )

    def process_response(self, response: str) -> dict[str, str]:
        """
        Process the user's confirmation response.
        """

        if self._pending_action is None:
            return {
                "status": "no_pending_confirmation",
                "message": "There is no pending confirmation.",
            }

        response = response.strip().lower()

        action = self._pending_action

        if SafetyManager.is_confirmation(response):
            self._pending_action = None

            return {
                "status": "confirmed",
                "action": action,
                "message": f"{action.capitalize()} confirmed.",
            }

        if SafetyManager.is_cancellation(response):
            self._pending_action = None

            return {
                "status": "cancelled",
                "action": action,
                "message": f"{action.capitalize()} cancelled.",
            }

        return {
            "status": "unclear",
            "action": action,
            "message": (
                "I didn't understand your response. "
                "Please say yes or no."
            ),
        }

    def cancel(self) -> None:
        """Cancel the current confirmation request."""

        self._pending_action = None