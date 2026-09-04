"""
Register all JARVIS tools.
"""

from __future__ import annotations

from ai.calculator import CalculatorTool
from ai.tool_registry import ToolRegistry
from ai.web_search_tool import WebSearchTool


def register_default_tools(registry: ToolRegistry) -> None:
    """Register all built-in JARVIS tools."""

    registry.register(CalculatorTool())
    registry.register(WebSearchTool())