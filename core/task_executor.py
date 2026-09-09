"""
Executor for JARVIS multi-step tasks.
"""

from __future__ import annotations

from collections.abc import Callable

from core.safety import SafetyManager
from core.task import Task, TaskStatus
from core.task_errors import TaskExecutionError


class TaskExecutor:
    """Execute task steps sequentially with safety checks."""

    def __init__(
        self,
        tool_router,
        confirmation_manager=None,
        confirmation_callback: Callable[[str], bool] | None = None,
    ):
        self.tool_router = tool_router
        self.confirmation_manager = confirmation_manager
        self.confirmation_callback = confirmation_callback

    def execute(self, task: Task) -> Task:
        task.status = TaskStatus.RUNNING

        for step in task.steps:
            step.status = TaskStatus.RUNNING

            try:
                arguments = dict(step.arguments)

                if self._requires_confirmation(step.action):
                    if self.confirmation_callback is None:
                        raise TaskExecutionError(
                            f"Confirmation required for action: "
                            f"{step.action}"
                        )

                    confirmed = self.confirmation_callback(step.action)

                    if not confirmed:
                        raise TaskExecutionError(
                            f"Action cancelled: {step.action}"
                        )

                    arguments["confirm"] = True

                result = self.tool_router.execute(
                    step.action,
                    arguments,
                )

                step.result = str(result)
                step.status = TaskStatus.COMPLETED

            except TaskExecutionError:
                step.status = TaskStatus.FAILED
                task.status = TaskStatus.FAILED
                raise

            except Exception as exc:
                step.error = str(exc)
                step.status = TaskStatus.FAILED
                task.status = TaskStatus.FAILED

                raise TaskExecutionError(
                    f"Task step '{step.action}' failed: {exc}"
                ) from exc

        task.status = TaskStatus.COMPLETED
        return task

    @staticmethod
    def _requires_confirmation(action: str) -> bool:
        return SafetyManager.requires_confirmation(action)