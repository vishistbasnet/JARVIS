from unittest.mock import patch

import pytest

from ai.system_control import SystemControlTool
from core.confirmation import ConfirmationManager


@pytest.fixture
def system_tool():
    return SystemControlTool()


@pytest.fixture
def confirmation():
    return ConfirmationManager()


def test_shutdown_requires_confirmation(system_tool):
    result = system_tool.execute("shutdown")

    assert result["status"] == "confirmation_required"
    assert result["action"] == "shutdown"


def test_restart_requires_confirmation(system_tool):
    result = system_tool.execute("restart")

    assert result["status"] == "confirmation_required"
    assert result["action"] == "restart"


def test_lock_does_not_require_confirmation(system_tool):
    with patch.object(system_tool, "_lock") as mock_lock:
        result = system_tool.execute("lock")

    assert result["status"] == "success"
    assert result["action"] == "lock"
    mock_lock.assert_called_once()


def test_sleep_does_not_require_confirmation(system_tool):
    with patch.object(system_tool, "_sleep") as mock_sleep:
        result = system_tool.execute("sleep")

    assert result["status"] == "success"
    assert result["action"] == "sleep"
    mock_sleep.assert_called_once()


def test_confirmation_without_pending_action(confirmation):
    result = confirmation.process_response("yes")

    assert result["status"] == "no_pending_confirmation"


def test_unclear_response_keeps_confirmation_pending(confirmation):
    confirmation.request_confirmation("shutdown")

    result = confirmation.process_response("maybe")

    assert result["status"] == "unclear"
    assert result["action"] == "shutdown"
    assert confirmation.pending_action == "shutdown"


def test_no_cancels_pending_action(confirmation):
    confirmation.request_confirmation("shutdown")

    result = confirmation.process_response("no")

    assert result["status"] == "cancelled"
    assert result["action"] == "shutdown"
    assert confirmation.pending_action is None


def test_confirmation_is_tied_to_pending_action(confirmation):
    confirmation.request_confirmation("restart")

    result = confirmation.process_response("yes")

    assert result["status"] == "confirmed"
    assert result["action"] == "restart"
    assert confirmation.pending_action is None


def test_confirmed_shutdown_executes_with_confirmation(system_tool):
    with patch.object(
        system_tool,
        "_shutdown",
    ) as mock_shutdown:

        result = system_tool.execute(
            action="shutdown",
            confirm=True,
        )

    assert result["status"] == "success"
    assert result["action"] == "shutdown"
    mock_shutdown.assert_called_once()


def test_confirmed_restart_executes_with_confirmation(system_tool):
    with patch.object(
        system_tool,
        "_restart",
    ) as mock_restart:

        result = system_tool.execute(
            action="restart",
            confirm=True,
        )

    assert result["status"] == "success"
    assert result["action"] == "restart"
    mock_restart.assert_called_once()
