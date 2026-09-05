"""
Register all JARVIS tools.
"""

from __future__ import annotations

from ai.app_launcher import AppLauncherTool
from ai.calculator import CalculatorTool
from ai.file_launcher import FileLauncherTool
from ai.system_control import SystemControlTool
from ai.tool_registry import ToolRegistry
from ai.web_search_tool import WebSearchTool
from ai.website_launcher import WebsiteLauncherTool


def register_default_tools(registry: ToolRegistry) -> None:
    """Register all built-in JARVIS tools."""

    registry.register(CalculatorTool())
    registry.register(WebSearchTool())
    registry.register(AppLauncherTool())
    registry.register(WebsiteLauncherTool())
    registry.register(FileLauncherTool())
    registry.register(SystemControlTool())