"""
Test SystemControlTool integration with SafetyManager.

This test NEVER performs shutdown or restart.
"""

from ai.system_control import SystemControlTool


def main() -> None:
    print("=" * 60)
    print("SYSTEM CONTROL + SAFETY INTEGRATION TEST")
    print("=" * 60)

    tool = SystemControlTool()

    print("\n1. Testing shutdown without confirmation...")

    result = tool.execute("shutdown")

    print(result)

    assert result["status"] == "confirmation_required"

    print("PASS")


    print("\n2. Testing restart without confirmation...")

    result = tool.execute("restart")

    print(result)

    assert result["status"] == "confirmation_required"

    print("PASS")


    print("\n3. Testing shutdown with confirmation...")

    print(
        "Skipping actual shutdown execution for safety."
    )

    # We only verify that SafetyManager allows the action.
    from core.safety import SafetyManager

    result = SafetyManager.check_action(
        "shutdown",
        confirm=True,
    )

    print(result)

    assert result["status"] == "allowed"

    print("PASS")


    print("\n4. Testing restart with confirmation...")

    print(
        "Skipping actual restart execution for safety."
    )

    result = SafetyManager.check_action(
        "restart",
        confirm=True,
    )

    print(result)

    assert result["status"] == "allowed"

    print("PASS")


    print("\n" + "=" * 60)
    print("SYSTEM CONTROL SAFETY TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()