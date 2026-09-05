from pathlib import Path
from unittest.mock import patch

import pytest

from ai.file_launcher import FileLauncherTool


def test_file_launcher_opens_downloads():
    tool = FileLauncherTool()

    expected_path = Path.home() / "Downloads"

    with patch("ai.file_launcher.os.startfile") as mock_startfile:
        result = tool.execute(path="downloads")

    assert result["status"] == "success"
    assert result["path"] == str(expected_path)
    assert result["message"] == f"Opening {expected_path}."

    mock_startfile.assert_called_once_with(
        str(expected_path)
    )


def test_file_launcher_opens_documents():
    tool = FileLauncherTool()

    expected_path = Path.home() / "Documents"

    with patch("ai.file_launcher.os.startfile") as mock_startfile:
        result = tool.execute(path="documents")

    assert result["status"] == "success"
    assert result["path"] == str(expected_path)

    mock_startfile.assert_called_once_with(
        str(expected_path)
    )


def test_file_launcher_accepts_existing_file_path(tmp_path):
    tool = FileLauncherTool()

    test_file = tmp_path / "test.txt"
    test_file.write_text("JARVIS test file")

    with patch("ai.file_launcher.os.startfile") as mock_startfile:
        result = tool.execute(path=str(test_file))

    assert result["status"] == "success"
    assert result["path"] == str(test_file)

    mock_startfile.assert_called_once_with(
        str(test_file)
    )


def test_file_launcher_rejects_empty_path():
    tool = FileLauncherTool()

    with patch("ai.file_launcher.os.startfile") as mock_startfile:
        with pytest.raises(
            ValueError,
            match="File or folder path cannot be empty",
        ):
            tool.execute(path="")

    mock_startfile.assert_not_called()


def test_file_launcher_rejects_missing_path(tmp_path):
    tool = FileLauncherTool()

    missing_path = tmp_path / "does_not_exist.txt"

    with patch("ai.file_launcher.os.startfile") as mock_startfile:
        with pytest.raises(
            FileNotFoundError,
            match="File or folder does not exist",
        ):
            tool.execute(path=str(missing_path))

    mock_startfile.assert_not_called()
