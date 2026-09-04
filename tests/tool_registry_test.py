"""
Tests for the JARVIS tool registry.
"""

from ai.tool_registry import ToolRegistry
from ai.tools import Tool


class TestTool(Tool):
    """Simple test tool."""

    name = "test_tool"
    description = "A tool used for testing."

    def execute(self, **kwargs):
        return "Tool executed successfully."


class CalculatorTestTool(Tool):
    """Second test tool."""

    name = "calculator"
    description = "Performs calculations."

    def execute(self, **kwargs):
        return 42


def main() -> None:
    print("=" * 60)
    print("         JARVIS TOOL REGISTRY TEST")
    print("=" * 60)

    registry = ToolRegistry()

    tool_1 = TestTool()
    tool_2 = CalculatorTestTool()

    print("\nRegistering tools...")

    registry.register(tool_1)
    registry.register(tool_2)

    print("✅ Tools registered.")

    print("\nAvailable tools:")

    for name in registry.list_tools():
        print(f"- {name}")

    assert registry.has("test_tool")
    assert registry.has("calculator")

    print("\nTesting tool retrieval...")

    retrieved = registry.get("test_tool")

    assert retrieved.name == "test_tool"
    assert retrieved.execute() == "Tool executed successfully."

    print("✅ Tool retrieval working.")

    print("\nTesting calculator tool...")

    calculator = registry.get("calculator")

    assert calculator.execute() == 42

    print("✅ Calculator tool retrieval working.")

    print("\nTesting duplicate registration...")

    try:
        registry.register(tool_1)
        raise AssertionError(
            "Duplicate registration should have failed."
        )
    except ValueError:
        print("✅ Duplicate registration correctly rejected.")

    print("\nTesting missing tool...")

    try:
        registry.get("unknown_tool")
        raise AssertionError(
            "Missing tool should have raised KeyError."
        )
    except KeyError:
        print("✅ Missing tool correctly rejected.")

    print("\n" + "=" * 60)
    print("✅ TOOL REGISTRY TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    