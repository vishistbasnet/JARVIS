import pytest

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


@pytest.fixture
def registry():
    registry = ToolRegistry()

    registry.register(TestTool())
    registry.register(CalculatorTestTool())

    return registry


def test_registered_tools_are_available(registry):
    assert registry.has("test_tool")
    assert registry.has("calculator")


def test_list_tools(registry):
    assert registry.list_tools() == [
        "test_tool",
        "calculator",
    ]


def test_get_tool(registry):
    tool = registry.get("test_tool")

    assert tool.name == "test_tool"
    assert tool.execute() == "Tool executed successfully."


def test_get_calculator_tool(registry):
    calculator = registry.get("calculator")

    assert calculator.execute() == 42


def test_duplicate_registration_is_rejected(registry):
    with pytest.raises(ValueError, match="Tool already registered"):
        registry.register(TestTool())


def test_missing_tool_is_rejected(registry):
    with pytest.raises(KeyError, match="Tool not found"):
        registry.get("unknown_tool")


def test_registry_has_returns_false_for_missing_tool(registry):
    assert registry.has("unknown_tool") is False
