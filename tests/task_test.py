"""
Tests for JARVIS task models.
"""

from core.task import Task, TaskStatus, TaskStep


def test_task_step_defaults():
    step = TaskStep(action="web_search")

    assert step.action == "web_search"
    assert step.arguments == {}
    assert step.status == TaskStatus.PENDING
    assert step.result is None
    assert step.error is None


def test_task_defaults():
    task = Task(goal="Search AI news")

    assert task.goal == "Search AI news"
    assert task.steps == []
    assert task.status == TaskStatus.PENDING


def test_task_step_accepts_arguments():
    step = TaskStep(
        action="web_search",
        arguments={"query": "AI news"},
    )

    assert step.arguments["query"] == "AI news"


def test_task_accepts_multiple_steps():
    task = Task(
        goal="Search and summarize",
        steps=[
            TaskStep(action="web_search"),
            TaskStep(action="summarize"),
        ],
    )

    assert len(task.steps) == 2
    assert task.steps[0].action == "web_search"
    assert task.steps[1].action == "summarize"


def test_task_status_can_change():
    task = Task(goal="Test task")

    task.status = TaskStatus.RUNNING

    assert task.status == TaskStatus.RUNNING