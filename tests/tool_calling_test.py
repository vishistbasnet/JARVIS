"""
Tests for the JARVIS Gemini tool-calling layer.
"""

from ai.tool_calling import GeminiToolCaller


def main() -> None:
    print("=" * 60)
    print("         JARVIS TOOL CALLING TEST")
    print("=" * 60)

    print("\nInitializing Gemini tool caller...")

    caller = GeminiToolCaller()

    print("✅ Tool caller initialized.")

    print("\nAvailable tools:")

    for name in caller.registry.list_tools():
        print(f"- {name}")

    assert caller.registry.has("calculator")

    print("✅ Calculator registered.")

    print("\nTesting calculator execution...")

    result = caller.calculate("25 * 4")

    print(f"25 * 4 = {result}")

    assert result == 100

    print("✅ Calculator execution successful.")

    print("\nTesting another calculation...")

    result = caller.calculate(
        "(100 + 50) / 5"
    )

    print(f"(100 + 50) / 5 = {result}")

    assert result == 30

    print("✅ Second calculation successful.")

    print("\n" + "=" * 60)
    print("✅ TOOL CALLING LAYER TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()