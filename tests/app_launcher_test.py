from unittest.mock import patch

from ai.app_launcher import AppLauncherTool


def test_app_launcher_opens_notepad():
    tool = AppLauncherTool()

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        result = tool.execute(application="notepad")

    assert result["status"] == "success"
    assert result["application"] == "notepad"
    assert result["message"] == "Opening notepad."

    mock_startfile.assert_called_once_with("notepad.exe")


def test_app_launcher_supports_calculator():
    tool = AppLauncherTool()

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        result = tool.execute(application="calculator")

    assert result["status"] == "success"
    assert result["application"] == "calculator"

    mock_startfile.assert_called_once_with("calc.exe")


def test_app_launcher_supports_aliases():
    tool = AppLauncherTool()

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        result = tool.execute(application="calc")

    assert result["status"] == "success"
    assert result["application"] == "calc"

    mock_startfile.assert_called_once_with("calc.exe")


def test_app_launcher_rejects_empty_application():
    tool = AppLauncherTool()

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        try:
            tool.execute(application="")
        except ValueError as exc:
            assert str(exc) == "Application name cannot be empty."
        else:
            raise AssertionError("Expected ValueError.")

    mock_startfile.assert_not_called()


def test_app_launcher_rejects_unsupported_application():
    tool = AppLauncherTool()

    with patch("ai.app_launcher.os.startfile") as mock_startfile:
        try:
            tool.execute(application="chrome")
        except ValueError as exc:
            assert "Application is not supported" in str(exc)
        else:
            raise AssertionError("Expected ValueError.")

    mock_startfile.assert_not_called()
