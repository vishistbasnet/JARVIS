import pytest

from core.safety import SafetyManager


def test_safe_action_does_not_require_confirmation():
    result = SafetyManager.check_action("lock")

    assert result["status"] == "allowed"
    assert result["requires_confirmation"] is False


def test_shutdown_requires_confirmation():
    result = SafetyManager.check_action("shutdown")

    assert result["status"] == "confirmation_required"
    assert result["requires_confirmation"] is True


def test_shutdown_with_confirmation_is_allowed():
    result = SafetyManager.check_action(
        "shutdown",
        confirm=True,
    )

    assert result["status"] == "allowed"


def test_restart_requires_confirmation():
    result = SafetyManager.check_action("restart")

    assert result["status"] == "confirmation_required"
    assert result["requires_confirmation"] is True


@pytest.mark.parametrize(
    "response",
    [
        "yes",
        "YES",
        "go ahead",
    ],
)
def test_confirmation_responses(response):
    assert SafetyManager.is_confirmation(response) is True


@pytest.mark.parametrize(
    "response",
    [
        "no",
        "cancel",
        "stop",
    ],
)
def test_cancellation_responses(response):
    assert SafetyManager.is_cancellation(response) is True
