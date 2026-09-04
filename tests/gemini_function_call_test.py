"""
Test Gemini's ability to request the JARVIS calculator tool.
"""

from ai.tool_calling import GeminiToolCaller


def main() -> None:
    print("=" * 60)
    print("       JARVIS GEMINI FUNCTION CALL TEST")
    print("=" * 60)

    caller = GeminiToolCaller()

    question = (
        "What is 125 multiplied by 8?"
    )

    print("\nUSER:")
    print(question)

    print("\nAsking Gemini whether a tool is needed...")

    function_call = caller.request_tool_call(
        question
    )

    assert function_call is not None

    print("\nGemini requested:")

    print(
        f"Tool: {function_call.name}"
    )

    print(
        f"Arguments: {function_call.args}"
    )

    assert function_call.name == "calculator"

    expression = function_call.args.get(
        "expression"
    )

    assert expression

    print(
        f"\nExpression selected by Gemini: "
        f"{expression}"
    )

    print("\nExecuting tool call...")

    result = caller.execute_tool_call(
        function_call
    )

    print(f"Calculator result: {result}")

    assert result == 1000

    print("\n" + "=" * 60)
    print("✅ GEMINI FUNCTION CALL TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    