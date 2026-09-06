from types import SimpleNamespace
from unittest.mock import patch

from ai.tool_calling import GeminiToolCaller


def test_gemini_cannot_authorize_shutdown():
    caller = GeminiToolCaller()

    function_call = SimpleNamespace(
        name="system_control",
        args={
            "action": "shutdown",
            "confirm": True,
        },
    )

    with patch.object(
        caller.router,
        "execute",
        return_value={
            "status": "confirmation_required",
            "action": "shutdown",
            "message": "Confirmation is required before shutdown.",
        },
    ) as mock_execute:

        result = caller.execute_tool_call(function_call)

    assert result["status"] == "confirmation_required"

    mock_execute.assert_called_once_with(
        "system_control",
        {
            "action": "shutdown",
            "confirm": False,
        },
    )


def test_gemini_cannot_authorize_restart():
    caller = GeminiToolCaller()

    function_call = SimpleNamespace(
        name="system_control",
        args={
            "action": "restart",
            "confirm": True,
        },
    )

    with patch.object(
        caller.router,
        "execute",
        return_value={
            "status": "confirmation_required",
            "action": "restart",
            "message": "Confirmation is required before restart.",
        },
    ) as mock_execute:

        result = caller.execute_tool_call(function_call)

    assert result["status"] == "confirmation_required"

    mock_execute.assert_called_once_with(
        "system_control",
        {
            "action": "restart",
            "confirm": False,
        },
    )