"""
Manual test for Tavily web search.
"""

from ai.web_search import TavilySearchProvider


def main() -> None:
    print("=" * 50)
    print("JARVIS WEB SEARCH TEST")
    print("=" * 50)

    provider = TavilySearchProvider()

    query = "latest Python programming language news"

    print(f"\nSearching for: {query}\n")

    results = provider.search(
        query=query,
        max_results=3,
    )

    if not results:
        print("No results returned.")
        return

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Content: {result.content[:300]}...")

    print("\n" + "=" * 50)
    print("WEB SEARCH TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()
    