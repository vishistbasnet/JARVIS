from unittest.mock import patch

from ai.website_launcher import WebsiteLauncherTool


def test_website_launcher_opens_youtube():
    tool = WebsiteLauncherTool()

    with patch("ai.website_launcher.webbrowser.open") as mock_open:
        result = tool.execute(website="youtube")

    assert result["status"] == "success"
    assert result["website"] == "youtube"
    assert result["url"] == "https://www.youtube.com"
    assert result["message"] == "Opening youtube."

    mock_open.assert_called_once_with(
        "https://www.youtube.com"
    )


def test_website_launcher_opens_google():
    tool = WebsiteLauncherTool()

    with patch("ai.website_launcher.webbrowser.open") as mock_open:
        result = tool.execute(website="google")

    assert result["status"] == "success"
    assert result["website"] == "google"

    mock_open.assert_called_once_with(
        "https://www.google.com"
    )


def test_website_launcher_supports_x_alias():
    tool = WebsiteLauncherTool()

    with patch("ai.website_launcher.webbrowser.open") as mock_open:
        result = tool.execute(website="x")

    assert result["status"] == "success"
    assert result["website"] == "x"
    assert result["url"] == "https://x.com"

    mock_open.assert_called_once_with(
        "https://x.com"
    )


def test_website_launcher_rejects_empty_website():
    tool = WebsiteLauncherTool()

    with patch("ai.website_launcher.webbrowser.open") as mock_open:
        try:
            tool.execute(website="")
        except ValueError as exc:
            assert str(exc) == "Website name cannot be empty."
        else:
            raise AssertionError("Expected ValueError.")

    mock_open.assert_not_called()


def test_website_launcher_rejects_unsupported_website():
    tool = WebsiteLauncherTool()

    with patch("ai.website_launcher.webbrowser.open") as mock_open:
        try:
            tool.execute(website="example")
        except ValueError as exc:
            assert "Website is not supported" in str(exc)
        else:
            raise AssertionError("Expected ValueError.")

    mock_open.assert_not_called()
