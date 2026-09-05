"""
Website launcher tool for JARVIS.

Provides safe opening of approved websites in the default browser.
"""

from __future__ import annotations

import webbrowser
from typing import Any

from ai.tools import Tool


class WebsiteLauncherTool(Tool):
    """Open approved websites in the default browser."""

    name = "website_launcher"

    description = (
        "Open a website in the user's default browser. "
        "Use this when the user asks to open a website or web service."
    )

    WEBSITES: dict[str, str] = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "gmail": "https://mail.google.com",
        "stackoverflow": "https://stackoverflow.com",
        "reddit": "https://www.reddit.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "x": "https://x.com",
    }

    def execute(
        self,
        website: str,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Open an approved website.

        Args:
            website: Website name or supported alias.

        Returns:
            A structured result describing the action.
        """

        website = website.strip().lower()

        if not website:
            raise ValueError("Website name cannot be empty.")

        url = self.WEBSITES.get(website)

        if url is None:
            raise ValueError(
                f"Website is not supported: {website}"
            )

        webbrowser.open(url)

        return {
            "status": "success",
            "website": website,
            "url": url,
            "message": f"Opening {website}.",
        }