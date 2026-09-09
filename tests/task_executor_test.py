import pytest

from core.task import Task, TaskStatus, TaskStep
from core.task_errors import TaskExecutionError
from core.task_executor import TaskExecutor
from core.confirmation import ConfirmationManager
from core.task_errors import TaskExecutionError
from unittest.mock import Mock

class FakeToolRouter:
    def __init__(self):
        self.calls = []

    def execute(self, action, arguments):
        self.calls.append((action, arguments))
        return f"Executed {action}"


class FailingToolRouter:
    def execute(self, action, arguments):
        raise RuntimeError("Tool failed")


def test_executor_runs_single_step():
    router = FakeToolRouter()
    executor = TaskExecutor(router)

    task = Task(
        goal="Search AI news",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI news"},
            )
        ],
    )

    result = executor.execute(task)

    assert result.status == TaskStatus.COMPLETED
    assert result.steps[0].status == TaskStatus.COMPLETED
    assert result.steps[0].result == "Executed web_search"


def test_executor_runs_steps_in_order():
    router = FakeToolRouter()
    executor = TaskExecutor(router)

    task = Task(
        goal="Search and open result",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI"},
            ),
            TaskStep(
                action="open_application",
                arguments={"application": "browser"},
            ),
        ],
    )

    result = executor.execute(task)

    assert result.status == TaskStatus.COMPLETED
    assert router.calls == [
        ("web_search", {"query": "AI"}),
        ("open_application", {"application": "browser"}),
    ]


def test_executor_raises_task_execution_error():
    router = FailingToolRouter()
    executor = TaskExecutor(router)

    task = Task(
        goal="Run failing task",
        steps=[
            TaskStep(action="web_search"),
            TaskStep(action="open_application"),
        ],
    )

    with pytest.raises(TaskExecutionError, match="Tool failed"):
        executor.execute(task)

    assert task.status == TaskStatus.FAILED
    assert task.steps[0].status == TaskStatus.FAILED
    assert task.steps[0].error == "Tool failed"
    assert task.steps[1].status == TaskStatus.PENDING

def test_executor_rejects_dangerous_action_without_confirmation():
    router = FakeToolRouter()
    confirmation = ConfirmationManager()

    executor = TaskExecutor(
        router,
        confirmation_manager=confirmation,
    )

    task = Task(
        goal="Shutdown computer",
        steps=[
            TaskStep(
                action="shutdown",
                arguments={},
            )
        ],
    )

    with pytest.raises(
        TaskExecutionError,
        match="Confirmation required",
    ):
        executor.execute(task)

    assert task.status == TaskStatus.FAILED
    assert task.steps[0].status == TaskStatus.FAILED
    assert router.calls == []


def test_executor_allows_normal_actions():
    router = FakeToolRouter()
    confirmation = ConfirmationManager()

    executor = TaskExecutor(
        router,
        confirmation_manager=confirmation,
    )

    task = Task(
        goal="Search AI news",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI news"},
            )
        ],
    )

    result = executor.execute(task)

    assert result.status == TaskStatus.COMPLETED
    assert result.steps[0].status == TaskStatus.COMPLETED
    assert router.calls == [
        ("web_search", {"query": "AI news"})
    ]

def test_executor_confirms_dangerous_action():
    router = Mock()
    router.execute.return_value = "Shutdown executed"

    confirmation_callback = Mock(return_value=True)

    executor = TaskExecutor(
        tool_router=router,
        confirmation_callback=confirmation_callback,
    )

    task = Task(
        goal="Shutdown computer",
        steps=[
            TaskStep(
                action="shutdown",
            )
        ],
    )

    result = executor.execute(task)

    assert result.status == TaskStatus.COMPLETED
    confirmation_callback.assert_called_once_with("shutdown")
    router.execute.assert_called_once_with(
        "shutdown",
        {"confirm": True},
    )


def test_executor_cancels_dangerous_action():
    router = Mock()
    confirmation_callback = Mock(return_value=False)

    executor = TaskExecutor(
        tool_router=router,
        confirmation_callback=confirmation_callback,
    )

    task = Task(
        goal="Shutdown computer",
        steps=[
            TaskStep(
                action="shutdown",
            )
        ],
    )

    with pytest.raises(TaskExecutionError, match="Action cancelled"):
        executor.execute(task)

    confirmation_callback.assert_called_once_with("shutdown")
    router.execute.assert_not_called()