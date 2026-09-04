"""
Test Gemini web search tool calling.
"""

from ai.tool_calling import GeminiToolCaller


def main() -> None:
    print("=" * 50)
    print("JARVIS GEMINI WEB SEARCH TEST")
    print("=" * 50)

    caller = GeminiToolCaller()

    message = (
        "What are the latest developments in Python "
        "programming in 2026?"
    )

    print(f"\nUser request:\n{message}")

    print("\nAsking Gemini whether web search is required...")

    response, function_call = caller.request_tool_call(
        message
    )

    assert function_call is not None, (
        "Gemini did not request a tool."
    )

    print(
        f"\nGemini selected tool: "
        f"{function_call.name}"
    )

    print(
        f"Arguments: "
        f"{function_call.args}"
    )

    assert function_call.name == "web_search"

    print("\nExecuting web search...")

    tool_result = caller.execute_tool_call(
        function_call
    )

    assert isinstance(tool_result, list)
    assert len(tool_result) > 0

    print(
        f"\nSearch results returned: "
        f"{len(tool_result)}"
    )

    for index, result in enumerate(
        tool_result,
        start=1,
    ):
        print(f"\n--- Result {index} ---")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(
            f"Content: "
            f"{result['content'][:200]}..."
        )

    print("\nGenerating final Gemini response...")

    final_response = caller.generate_final_response(
        message=message,
        response=response,
        tool_result=tool_result,
    )

    assert final_response

    print("\n--- Final JARVIS Response ---")
    print(final_response)

    print("\n" + "=" * 50)
    print("GEMINI WEB SEARCH TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()