from types import SimpleNamespace
from unittest.mock import patch

from ai.web_search_tool import WebSearchTool


def test_web_search_tool_returns_formatted_results():
    fake_results = [
        SimpleNamespace(
            title="Python News",
            url="https://example.com/python",
            content="Latest Python programming news.",
        ),
        SimpleNamespace(
            title="Python 2026",
            url="https://example.com/python-2026",
            content="Python developments in 2026.",
        ),
    ]

    tool = WebSearchTool()

    with patch.object(
        tool.provider,
        "search",
        return_value=fake_results,
    ) as mock_search:

        results = tool.execute(
            query="latest Python programming language news",
            max_results=3,
        )

    assert isinstance(results, list)
    assert len(results) == 2

    assert results[0] == {
        "title": "Python News",
        "url": "https://example.com/python",
        "content": "Latest Python programming news.",
    }

    assert results[1] == {
        "title": "Python 2026",
        "url": "https://example.com/python-2026",
        "content": "Python developments in 2026.",
    }

    mock_search.assert_called_once_with(
        query="latest Python programming language news",
        max_results=3,
    )


def test_web_search_tool_handles_empty_results():
    tool = WebSearchTool()

    with patch.object(
        tool.provider,
        "search",
        return_value=[],
    ) as mock_search:

        results = tool.execute(
            query="some query",
            max_results=3,
        )

    assert results == []

    mock_search.assert_called_once_with(
        query="some query",
        max_results=3,
    )
