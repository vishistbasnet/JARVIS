import pytest
from unittest.mock import patch

from ai.system_control import SystemControlTool


@pytest.fixture
def tool():
    return SystemControlTool()


def test_invalid_action_is_rejected(tool):
    with pytest.raises(
        ValueError,
        match="Unsupported system action",
    ):
        tool.execute("invalid")


def test_shutdown_requires_confirmation(tool):
    result = tool.execute("shutdown")

    assert result["status"] == "confirmation_required"
    assert result["action"] == "shutdown"


def test_restart_requires_confirmation(tool):
    result = tool.execute("restart")

    assert result["status"] == "confirmation_required"
    assert result["action"] == "restart"


def test_lock_does_not_require_confirmation(tool):
    with patch.object(tool, "_lock") as mock_lock:
        result = tool.execute("lock")

    assert result["status"] == "success"
    assert result["action"] == "lock"
    mock_lock.assert_called_once()


def test_sleep_does_not_require_confirmation(tool):
    with patch.object(tool, "_sleep") as mock_sleep:
        result = tool.execute("sleep")

    assert result["status"] == "success"
    assert result["action"] == "sleep"
    mock_sleep.assert_called_once()
