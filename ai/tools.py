"""
Tool system for JARVIS.

Tools are small, reusable actions that JARVIS can execute.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """Base interface for every JARVIS tool."""

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """
        Execute the tool.

        Each concrete tool defines its own arguments and behavior.
        """
        raise NotImplementedError