"""
Errors related to JARVIS task execution.
"""

from __future__ import annotations


class TaskExecutionError(RuntimeError):
    """Raised when a task step cannot be executed."""