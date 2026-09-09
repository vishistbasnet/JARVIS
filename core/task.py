"""
Task models for JARVIS multi-step execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    """Possible states of a task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class TaskStep:
    """A single step within a task."""

    action: str
    arguments: dict = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None
    error: str | None = None


@dataclass(slots=True)
class Task:
    """A multi-step task."""

    goal: str
    steps: list[TaskStep] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING