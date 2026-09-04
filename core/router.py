"""
Tool router for JARVIS.

The router connects tool decisions to registered tools.
"""

from __future__ import annotations

from typing import Any

from ai.tool_registry import ToolRegistry
from utils.logger import get_logger


logger = get_logger(__name__)


class ToolRouter:
    """Route tool requests to registered tools."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute a registered tool.

        Args:
            tool_name: Name of the tool to execute.
            arguments: Arguments passed to the tool.

        Returns:
            Result returned by the tool.
        """

        if not tool_name.strip():
            raise ValueError("Tool name cannot be empty.")

        arguments = arguments or {}

        logger.info(
            "Routing tool request: %s",
            tool_name,
        )

        tool = self.registry.get(tool_name)

        result = tool.execute(**arguments)

        logger.info(
            "Tool '%s' executed successfully.",
            tool_name,
        )

        return result