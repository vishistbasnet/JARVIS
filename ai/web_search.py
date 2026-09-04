"""
Web search functionality for JARVIS.

Provides a provider-independent interface for web search.
"""

from __future__ import annotations

from dataclasses import dataclass

from tavily import TavilyClient

from config import settings


@dataclass
class SearchResult:
    """Represents one web search result."""

    title: str
    url: str
    content: str


class WebSearchProvider:
    """Base interface for web search providers."""

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search the web."""
        raise NotImplementedError


class TavilySearchProvider(WebSearchProvider):
    """Web search provider powered by Tavily."""

    def __init__(self) -> None:
        if not settings.tavily_api_key:
            raise ValueError(
                "TAVILY_API_KEY is not configured."
            )

        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search the web using Tavily."""

        query = query.strip()

        if not query:
            raise ValueError(
                "Search query cannot be empty."
            )

        if max_results < 1:
            raise ValueError(
                "max_results must be at least 1."
            )

        response = self.client.search(
            query=query,
            max_results=max_results,
        )

        results: list[SearchResult] = []

        for item in response.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content", ""),
                )
            )

        return results