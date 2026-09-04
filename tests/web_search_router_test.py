"""
Test WebSearchTool through the JARVIS ToolRouter.
"""

from ai.register_tools import register_default_tools
from ai.tool_registry import ToolRegistry
from core.router import ToolRouter


def main() -> None:
    print("=" * 50)
    print("JARVIS WEB SEARCH ROUTER TEST")
    print("=" * 50)

    print("\nCreating tool registry...")
    registry = ToolRegistry()

    print("Registering default tools...")
    register_default_tools(registry)

    print("Creating tool router...")
    router = ToolRouter(registry)

    print("\nAvailable tools:")

    for tool_name in registry.list_tools():
        print(f"- {tool_name}")

    query = "What are the latest Python developments in 2026?"

    print(f"\nSearch query: {query}")
    print("Routing request to: web_search")

    results = router.execute(
        tool_name="web_search",
        arguments={
            "query": query,
            "max_results": 3,
        },
    )

    print(f"\nResults returned: {len(results)}")

    assert isinstance(results, list)
    assert len(results) > 0

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content'][:250]}...")

        assert "title" in result
        assert "url" in result
        assert "content" in result

    print("\nWeb search successfully executed through ToolRouter.")

    print("\n" + "=" * 50)
    print("WEB SEARCH ROUTER TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()