"""
Test WebSearchTool registration.
"""

from ai.tool_registry import ToolRegistry
from ai.register_tools import register_default_tools


def main() -> None:
    print("=" * 50)
    print("JARVIS WEB SEARCH REGISTRY TEST")
    print("=" * 50)

    registry = ToolRegistry()

    register_default_tools(registry)

    tools = registry.list_tools()

    print("\nRegistered tools:")

    for tool in tools:
        print(f"- {tool}")

    assert registry.has("calculator")
    assert registry.has("web_search")

    web_search = registry.get("web_search")

    assert web_search.name == "web_search"

    print("\nWeb search tool successfully registered.")

    print("\n" + "=" * 50)
    print("WEB SEARCH REGISTRY TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()