from ai.register_tools import register_default_tools
from ai.tool_registry import ToolRegistry


def test_web_search_tool_is_registered():
    registry = ToolRegistry()

    register_default_tools(registry)

    assert registry.has("calculator")
    assert registry.has("web_search")

    web_search = registry.get("web_search")

    assert web_search.name == "web_search"
