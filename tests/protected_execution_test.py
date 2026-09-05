from unittest.mock import patch

from core.assistant import Assistant


def test_confirmed_shutdown_uses_confirmation_flag():
    assistant = Assistant()

    system_tool = assistant.tool_caller.registry.get(
        "system_control"
    )

    with patch.object(
        system_tool,
        "execute",
        return_value={
            "status": "success",
            "action": "shutdown",
            "message": "System shutdown initiated.",
        },
    ) as mock_execute:

        result = assistant._execute_confirmed_action(
            action="shutdown"
        )

    assert result == "System shutdown initiated."

    mock_execute.assert_called_once_with(
        action="shutdown",
        confirm=True,
    )


def test_confirmed_restart_uses_confirmation_flag():
    assistant = Assistant()

    system_tool = assistant.tool_caller.registry.get(
        "system_control"
    )

    with patch.object(
        system_tool,
        "execute",
        return_value={
            "status": "success",
            "action": "restart",
            "message": "System restart initiated.",
        },
    ) as mock_execute:

        result = assistant._execute_confirmed_action(
            action="restart"
        )

    assert result == "System restart initiated."

    mock_execute.assert_called_once_with(
        action="restart",
        confirm=True,
    )
