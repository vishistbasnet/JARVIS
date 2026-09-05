import pytest

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


@pytest.fixture
def router():
    registry = ToolRegistry()

    registry.register(TestTool())
    registry.register(CalculatorTestTool())

    return ToolRouter(registry)


def test_basic_tool_routing(router):
    result = router.execute(
        "test_tool",
        {"message": "Hello JARVIS"},
    )

    assert result == "Executed: Hello JARVIS"


def test_router_passes_arguments(router):
    result = router.execute(
        "calculator",
        {
            "a": 10,
            "b": 32,
        },
    )

    assert result == 42


def test_unknown_tool_is_rejected(router):
    with pytest.raises(KeyError, match="Tool not found"):
        router.execute("unknown_tool")


def test_empty_tool_name_is_rejected(router):
    with pytest.raises(ValueError, match="Tool name cannot be empty"):
        router.execute("")
