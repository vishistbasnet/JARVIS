"""
File and folder launcher tool for JARVIS.

Provides safe access to common Windows user folders.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ai.tools import Tool


class FileLauncherTool(Tool):
    """Open approved Windows files and folders."""

    name = "file_launcher"

    description = (
        "Open a file or folder on the user's Windows computer. "
        "Use this when the user asks to open Downloads, Documents, "
        "Desktop, Pictures, Music, Videos, or another known location."
    )

    FOLDERS: dict[str, Path] = {
        "desktop": Path.home() / "Desktop",
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "pictures": Path.home() / "Pictures",
        "music": Path.home() / "Music",
        "videos": Path.home() / "Videos",
    }

    def execute(
        self,
        path: str,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Open an approved folder or file.

        Args:
            path: Folder name or path to open.

        Returns:
            Structured result describing the action.
        """

        path = path.strip()

        if not path:
            raise ValueError("File or folder path cannot be empty.")

        # Check whether the user requested a known folder.
        folder_path = self.FOLDERS.get(path.lower())

        if folder_path is not None:
            target = folder_path
        else:
            # Allow an explicitly supplied local path.
            target = Path(path).expanduser()

        if not target.exists():
            raise FileNotFoundError(
                f"File or folder does not exist: {target}"
            )

        os.startfile(str(target))

        return {
            "status": "success",
            "path": str(target),
            "message": f"Opening {target}.",
        }