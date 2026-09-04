"""
Test for the JARVIS web search tool.
"""

from ai.web_search_tool import WebSearchTool


def main() -> None:
    print("=" * 50)
    print("JARVIS WEB SEARCH TOOL TEST")
    print("=" * 50)

    tool = WebSearchTool()

    print(f"\nTool name: {tool.name}")
    print(f"Description: {tool.description}")

    query = "latest Python programming language news"

    print(f"\nQuery: {query}")
    print("\nExecuting web_search tool...")

    results = tool.execute(
        query=query,
        max_results=3,
    )

    print(f"\nResults returned: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content'][:200]}...")

    assert isinstance(results, list)
    assert len(results) > 0

    for result in results:
        assert "title" in result
        assert "url" in result
        assert "content" in result

    print("\n" + "=" * 50)
    print("WEB SEARCH TOOL TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()