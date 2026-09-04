
"""
JARVIS web search tool.

Wraps the web search provider as a standard JARVIS tool.
"""

from __future__ import annotations

from typing import Any

from ai.tools import Tool
from ai.web_search import TavilySearchProvider


class WebSearchTool(Tool):
    """Search the web using Tavily."""

    name = "web_search"

    description = (
        "Searches the internet for current information. "
        "Use this when the user asks about recent events, "
        "current information, news, or information that may "
        "have changed over time."
    )

    def __init__(self) -> None:
        self.provider = TavilySearchProvider()

    def execute(
        self,
        query: str,
        max_results: int = 5,
        **kwargs: Any,
    ) -> list[dict[str, str]]:
        """Execute a web search."""

        results = self.provider.search(
            query=query,
            max_results=max_results,
        )

        return [
            {
                "title": result.title,
                "url": result.url,
                "content": result.content,
            }
            for result in results
        ]