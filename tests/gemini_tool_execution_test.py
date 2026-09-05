from unittest.mock import patch

from ai.tool_calling import GeminiToolCaller


def test_tool_execution():
    caller = GeminiToolCaller()

    _, function_call = caller.request_tool_call(
        "Open Notepad."
    )

    assert function_call is not None
    assert function_call.name == "app_launcher"

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        result = caller.execute_tool_call(function_call)

    assert result["status"] == "success"
    assert result["application"] == "notepad"

    mock_startfile.assert_called_once_with("notepad.exe")
