"""
System control tool for JARVIS.

Provides controlled Windows system actions.
"""

from __future__ import annotations

import ctypes
import subprocess
from typing import Any

from ai.tools import Tool
from core.safety import SafetyManager


class SystemControlTool(Tool):
    """Perform controlled Windows system actions."""

    name = "system_control"

    description = (
        "Control the Windows computer with actions such as locking, "
        "sleeping, shutting down, or restarting the system."
    )

    ACTIONS = {
        "lock",
        "sleep",
        "shutdown",
        "restart",
    }

    def execute(
        self,
        action: str,
        confirm: bool = False,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Execute a Windows system control action.

        Dangerous actions require explicit confirmation.
        """

        action = action.strip().lower()

        if not action:
            raise ValueError("System action cannot be empty.")

        if action not in self.ACTIONS:
            raise ValueError(
                f"Unsupported system action: {action}"
            )

        safety_result = SafetyManager.check_action(
            action=action,
            confirm=confirm,
        )

        if safety_result["status"] == "confirmation_required":
            return {
                "status": "confirmation_required",
                "action": action,
                "message": safety_result["message"],
            }

        if action == "lock":
            self._lock()

            return {
                "status": "success",
                "action": "lock",
                "message": "Computer locked successfully.",
            }

        if action == "sleep":
            self._sleep()

            return {
                "status": "success",
                "action": "sleep",
                "message": "Computer entering sleep mode.",
            }

        if action == "shutdown":
            self._shutdown()

            return {
                "status": "success",
                "action": "shutdown",
                "message": "System shutdown initiated.",
            }

        if action == "restart":
            self._restart()

            return {
                "status": "success",
                "action": "restart",
                "message": "System restart initiated.",
            }

        raise RuntimeError("Unexpected system action.")

    @staticmethod
    def _lock() -> None:
        """Lock the Windows workstation."""

        result = ctypes.windll.user32.LockWorkStation()

        if result == 0:
            raise RuntimeError(
                "Failed to lock the computer."
            )

    @staticmethod
    def _sleep() -> None:
        """Put Windows into sleep mode."""

        subprocess.run(
            [
                "rundll32.exe",
                "powrprof.dll,SetSuspendState",
                "0,1,0",
            ],
            check=True,
        )

    @staticmethod
    def _shutdown() -> None:
        """Shut down Windows."""

        subprocess.run(
            ["shutdown", "/s", "/t", "0"],
            check=True,
        )

    @staticmethod
    def _restart() -> None:
        """Restart Windows."""

        subprocess.run(
            ["shutdown", "/r", "/t", "0"],
            check=True,
        )