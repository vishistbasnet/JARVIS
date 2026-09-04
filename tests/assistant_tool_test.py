"""
Integration test for Assistant tool calling.

Tests the calculator tool through the Gemini tool-calling
pipeline without using microphone or speaker hardware.
"""

from ai.tool_calling import GeminiToolCaller


def main() -> None:
    print("=" * 60)
    print("        JARVIS ASSISTANT TOOL INTEGRATION TEST")
    print("=" * 60)

    caller = GeminiToolCaller()

    question = (
        "What is 125 multiplied by 8?"
    )

    print("\nUSER:")
    print(question)

    print(
        "\nStep 1: Asking Gemini for tool decision..."
    )

    gemini_response, function_call = (
        caller.request_tool_call(
            question
        )
    )

    assert function_call is not None

    print(
        f"\nTool selected: "
        f"{function_call.name}"
    )

    print(
        f"Arguments: "
        f"{function_call.args}"
    )

    assert function_call.name == "calculator"

    print(
        "\nStep 2: Executing tool..."
    )

    tool_result = caller.execute_tool_call(
        function_call
    )

    print(
        f"Tool result: {tool_result}"
    )

    assert tool_result == 1000

    print(
        "\nStep 3: Generating final response..."
    )

    final_response = (
        caller.generate_final_response(
            message=question,
            response=gemini_response,
            tool_result=tool_result,
        )
    )

    print("\nJARVIS:")
    print(final_response)

    assert final_response

    print("\n" + "=" * 60)
    print("✅ ASSISTANT TOOL INTEGRATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()