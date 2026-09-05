from ai.register_tools import register_default_tools
from ai.tool_registry import ToolRegistry


def test_default_tools_are_registered():
    registry = ToolRegistry()

    register_default_tools(registry)

    expected_tools = {
        "calculator",
        "web_search",
        "app_launcher",
        "website_launcher",
        "file_launcher",
        "system_control",
    }

    actual_tools = set(registry.list_tools())

    assert actual_tools == expected_tools
    assert len(actual_tools) == 6
