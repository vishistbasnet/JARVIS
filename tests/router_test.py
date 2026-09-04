"""
Tests for the JARVIS tool router.
"""

from ai.tool_registry import ToolRegistry
from ai.tools import Tool
from core.router import ToolRouter


class TestTool(Tool):
    """Simple test tool."""

    name = "test_tool"
    description = "A tool used for testing."

    def execute(self, message: str = "default", **kwargs):
        return f"Executed: {message}"


class CalculatorTestTool(Tool):
    """Simple calculator test tool."""

    name = "calculator"
    description = "Performs a test calculation."

    def execute(self, a: int, b: int, **kwargs):
        return a + b


def main() -> None:
    print("=" * 60)
    print("             JARVIS ROUTER TEST")
    print("=" * 60)

    # Create registry.
    registry = ToolRegistry()

    # Register tools.
    registry.register(TestTool())
    registry.register(CalculatorTestTool())

    print("\nRegistered tools:")
    for name in registry.list_tools():
        print(f"- {name}")

    # Create router.
    router = ToolRouter(registry)

    print("\nTesting basic tool routing...")

    result = router.execute(
        "test_tool",
        {"message": "Hello JARVIS"},
    )

    print(f"Result: {result}")

    assert result == "Executed: Hello JARVIS"

    print("✅ Basic routing working.")

    print("\nTesting calculator routing...")

    result = router.execute(
        "calculator",
        {
            "a": 10,
            "b": 32,
        },
    )

    print(f"Result: {result}")

    assert result == 42

    print("✅ Argument passing working.")

    print("\nTesting unknown tool...")

    try:
        router.execute("unknown_tool")

        raise AssertionError(
            "Unknown tool should have failed."
        )

    except KeyError:
        print("✅ Unknown tool correctly rejected.")

    print("\nTesting empty tool name...")

    try:
        router.execute("")

        raise AssertionError(
            "Empty tool name should have failed."
        )

    except ValueError:
        print("✅ Empty tool name correctly rejected.")

    print("\n" + "=" * 60)
    print("✅ ROUTER TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()