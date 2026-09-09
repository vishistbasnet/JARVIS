import pytest

from core.plan_validator import PlanValidationError, PlanValidator
from core.task import Task, TaskStep


def test_valid_plan():
    task = Task(
        goal="Search AI news",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI news"},
            )
        ],
    )

    validator = PlanValidator()

    assert validator.validate(task) is True


def test_empty_goal_is_rejected():
    task = Task(
        goal="",
        steps=[TaskStep(action="web_search")],
    )

    validator = PlanValidator()

    with pytest.raises(PlanValidationError):
        validator.validate(task)


def test_plan_without_steps_is_rejected():
    task = Task(goal="Search AI news")

    validator = PlanValidator()

    with pytest.raises(PlanValidationError):
        validator.validate(task)


def test_empty_action_is_rejected():
    task = Task(
        goal="Search AI news",
        steps=[TaskStep(action="")],
    )

    validator = PlanValidator()

    with pytest.raises(PlanValidationError):
        validator.validate(task)


def test_non_dict_arguments_are_rejected():
    task = Task(
        goal="Search AI news",
        steps=[
            TaskStep(
                action="web_search",
                arguments="AI news",
            )
        ],
    )

    validator = PlanValidator()

    with pytest.raises(PlanValidationError):
        validator.validate(task)

def test_unknown_action_is_rejected():
    task = Task(
        goal="Do something",
        steps=[
            TaskStep(action="unknown_tool"),
        ],
    )

    validator = PlanValidator(
        allowed_actions={"web_search", "calculator"}
    )

    with pytest.raises(PlanValidationError, match="Unknown action"):
        validator.validate(task)


def test_allowed_action_is_accepted():
    task = Task(
        goal="Search AI news",
        steps=[
            TaskStep(
                action="web_search",
                arguments={"query": "AI news"},
            ),
        ],
    )

    validator = PlanValidator(
        allowed_actions={"web_search", "calculator"}
    )

    assert validator.validate(task)