"""
Tool registry for JARVIS.

The registry stores available tools and allows them
to be retrieved by name.
"""

from __future__ import annotations

from ai.tools import Tool


class ToolRegistry:
    """Registry for JARVIS tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool."""

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """Get a tool by name."""

        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(
                f"Tool not found: {name}"
            ) from exc

    def list_tools(self) -> list[str]:
        """Return the names of all registered tools."""

        return list(self._tools.keys())

    def has(self, name: str) -> bool:
        """Check whether a tool is registered."""

        return name in self._tools