"""
Basic tests for the JARVIS tool abstraction.
"""

from ai.tools import Tool


class TestTool(Tool):
    """Simple test tool."""

    name = "test_tool"
    description = "A tool used for testing."

    def execute(self, **kwargs):
        return "Tool executed successfully."


def main() -> None:
    print("=" * 60)
    print("             JARVIS TOOL TEST")
    print("=" * 60)

    tool = TestTool()

    print("\nTool name:")
    print(tool.name)

    print("\nTool description:")
    print(tool.description)

    result = tool.execute()

    print("\nExecution result:")
    print(result)

    assert tool.name == "test_tool"
    assert result == "Tool executed successfully."

    print("\n" + "=" * 60)
    print("✅ TOOL ABSTRACTION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()