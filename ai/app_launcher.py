"""
Application launcher tool for JARVIS.

Provides safe launching of known Windows applications.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ai.tools import Tool


class AppLauncherTool(Tool):
    """Launch approved Windows applications."""

    name = "app_launcher"

    description = (
        "Open a Windows application installed on the computer. "
        "Use this when the user asks to open, launch, or start an application."
    )

    # Common Windows applications.
    # These are aliases mapped to their executable paths/commands.
    APPLICATIONS: dict[str, str] = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
    }

    def execute(
        self,
        application: str,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Launch an approved Windows application.

        Args:
            application: Application name or supported alias.

        Returns:
            A structured result describing the action.
        """

        application = application.strip().lower()

        if not application:
            raise ValueError("Application name cannot be empty.")

        executable = self.APPLICATIONS.get(application)

        if executable is None:
            raise ValueError(
                f"Application is not supported: {application}"
            )

        os.startfile(executable)

        return {
            "status": "success",
            "application": application,
            "message": f"Opening {application}.",
        }