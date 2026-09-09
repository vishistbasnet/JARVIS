import pytest
from unittest.mock import Mock

from core.assistant import Assistant
from core.task import Task, TaskStep, TaskStatus


def test_should_create_plan_for_multi_step_request():
    assistant = Assistant.__new__(Assistant)

    assert assistant._should_create_plan(
        "Search for AI news and then open YouTube"
    )


def test_should_not_create_plan_for_simple_request():
    assistant = Assistant.__new__(Assistant)

    assert not assistant._should_create_plan(
        "Open YouTube"
    )


def test_should_detect_then():
    assistant = Assistant.__new__(Assistant)

    assert assistant._should_create_plan(
        "Search AI news then open YouTube"
    )


def test_process_planned_task():
    assistant = Assistant.__new__(Assistant)

    task = Task(
        goal="Search AI news and then open YouTube",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI news"},
                status=TaskStatus.COMPLETED,
                result="Search completed",
            ),
            TaskStep(
                action="website_launcher",
                arguments={"website": "YouTube"},
                status=TaskStatus.COMPLETED,
                result="YouTube opened",
            ),
        ],
        status=TaskStatus.COMPLETED,
    )

    assistant.planner = Mock()
    assistant.plan_validator = Mock()
    assistant.task_executor = Mock()

    assistant.planner.create_plan.return_value = task
    assistant.task_executor.execute.return_value = task

    response = assistant._process_planned_task(
        "Search AI news and then open YouTube"
    )

    assistant.planner.create_plan.assert_called_once()
    assistant.plan_validator.validate.assert_called_once_with(task)
    assistant.task_executor.execute.assert_called_once_with(task)

    assert "completed successfully" in response.lower()

def test_process_planned_task_rejects_invalid_plan():
    assistant = Assistant.__new__(Assistant)

    assistant.planner = Mock()
    assistant.plan_validator = Mock()
    assistant.task_executor = Mock()

    assistant.planner.create_plan.side_effect = ValueError(
        "Invalid planner response"
    )

    with pytest.raises(ValueError, match="Invalid planner response"):
        assistant._process_planned_task("Do something and then do something else")

    assistant.task_executor.execute.assert_not_called()


def test_process_planned_task_does_not_execute_invalid_plan():
    assistant = Assistant.__new__(Assistant)

    assistant.planner = Mock()
    assistant.plan_validator = Mock()
    assistant.task_executor = Mock()

    task = Task(
        goal="Search AI news and then open YouTube",
        steps=[
            TaskStep(
                action="unknown_tool",
            )
        ],
    )

    assistant.planner.create_plan.return_value = task
    assistant.plan_validator.validate.side_effect = ValueError(
        "Unknown action"
    )

    with pytest.raises(ValueError, match="Unknown action"):
        assistant._process_planned_task(
            "Search AI news and then open YouTube"
        )

    assistant.task_executor.execute.assert_not_called()