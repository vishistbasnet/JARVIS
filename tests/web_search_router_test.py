from unittest.mock import patch

from ai.register_tools import register_default_tools
from ai.tool_registry import ToolRegistry
from core.router import ToolRouter


def test_web_search_routes_through_tool_router():
    registry = ToolRegistry()
    register_default_tools(registry)

    router = ToolRouter(registry)

    expected_results = [
        {
            "title": "Python 2026 Developments",
            "url": "https://example.com/python-2026",
            "content": "Latest Python developments and updates.",
        },
        {
            "title": "Python Release News",
            "url": "https://example.com/python-release",
            "content": "Recent Python release information.",
        },
    ]

    with patch(
        "ai.web_search_tool.WebSearchTool.execute",
        return_value=expected_results,
    ) as mock_execute:

        results = router.execute(
            tool_name="web_search",
            arguments={
                "query": "What are the latest Python developments in 2026?",
                "max_results": 3,
            },
        )

    assert isinstance(results, list)
    assert len(results) == 2

    assert results == expected_results

    mock_execute.assert_called_once_with(
        query="What are the latest Python developments in 2026?",
        max_results=3,
    )


def test_web_search_results_have_expected_fields():
    registry = ToolRegistry()
    register_default_tools(registry)

    router = ToolRouter(registry)

    expected_results = [
        {
            "title": "Python News",
            "url": "https://example.com/python",
            "content": "Python information.",
        }
    ]

    with patch(
        "ai.web_search_tool.WebSearchTool.execute",
        return_value=expected_results,
    ):
        results = router.execute(
            tool_name="web_search",
            arguments={
                "query": "Python news",
                "max_results": 1,
            },
        )

    assert isinstance(results, list)

    for result in results:
        assert "title" in result
        assert "url" in result
        assert "content" in result
