"""
Validation for JARVIS task plans.
"""

from __future__ import annotations

from core.task import Task


class PlanValidationError(ValueError):
    """Raised when a task plan is invalid."""


class PlanValidator:
    """Validate tasks before they are executed."""

    def __init__(self, allowed_actions=None):
        self.allowed_actions = (
            set(allowed_actions) if allowed_actions is not None else None
        )

    def validate(self, task: Task) -> bool:
        if not task.goal.strip():
            raise PlanValidationError("Task goal cannot be empty.")

        if not task.steps:
            raise PlanValidationError(
                "Task must contain at least one step."
            )

        for index, step in enumerate(task.steps):
            if not step.action.strip():
                raise PlanValidationError(
                    f"Step {index + 1} must have an action."
                )

            if not isinstance(step.arguments, dict):
                raise PlanValidationError(
                    f"Arguments for step {index + 1} must be a dictionary."
                )

            if (
                self.allowed_actions is not None
                and step.action not in self.allowed_actions
            ):
                raise PlanValidationError(
                    f"Unknown action in step {index + 1}: "
                    f"{step.action}"
                )

        return True