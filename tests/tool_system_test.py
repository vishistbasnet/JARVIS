"""
End-to-end test for the JARVIS tool system.
"""

from ai.calculator import CalculatorTool
from ai.tool_registry import ToolRegistry
from core.router import ToolRouter


def main() -> None:
    print("=" * 60)
    print("          JARVIS TOOL SYSTEM TEST")
    print("=" * 60)

    print("\nCreating tool registry...")

    registry = ToolRegistry()

    print("Registering calculator...")

    calculator = CalculatorTool()
    registry.register(calculator)

    print("✅ Calculator registered.")

    print("\nCreating tool router...")

    router = ToolRouter(registry)

    print("✅ Router created.")

    print("\nAvailable tools:")

    for name in registry.list_tools():
        print(f"- {name}")

    print("\nTesting complete tool chain...")

    expression = "25 * 4 + 10"

    print(f"Expression: {expression}")

    result = router.execute(
        "calculator",
        {
            "expression": expression,
        },
    )

    print(f"Result: {result}")

    assert result == 110

    print("✅ Calculator executed through registry and router.")

    print("\nTesting another expression...")

    expression = "(100 + 50) / 5"

    print(f"Expression: {expression}")

    result = router.execute(
        "calculator",
        {
            "expression": expression,
        },
    )

    print(f"Result: {result}")

    assert result == 30

    print("✅ Second calculation successful.")

    print("\n" + "=" * 60)
    print("✅ COMPLETE TOOL SYSTEM TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()