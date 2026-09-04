"""
Tests for the JARVIS calculator tool.
"""

from ai.calculator import CalculatorTool


def main() -> None:
    print("=" * 60)
    print("           JARVIS CALCULATOR TEST")
    print("=" * 60)

    calculator = CalculatorTool()

    print("\nTesting addition...")

    result = calculator.execute("10 + 5")

    print(f"10 + 5 = {result}")

    assert result == 15

    print("✅ Addition working.")

    print("\nTesting multiplication...")

    result = calculator.execute("25 * 4")

    print(f"25 * 4 = {result}")

    assert result == 100

    print("✅ Multiplication working.")

    print("\nTesting division...")

    result = calculator.execute("100 / 5")

    print(f"100 / 5 = {result}")

    assert result == 20

    print("✅ Division working.")

    print("\nTesting parentheses...")

    result = calculator.execute(
        "(10 + 5) * 2"
    )

    print(f"(10 + 5) * 2 = {result}")

    assert result == 30

    print("✅ Parentheses working.")

    print("\nTesting power...")

    result = calculator.execute("2 ** 5")

    print(f"2 ** 5 = {result}")

    assert result == 32

    print("✅ Power operation working.")

    print("\nTesting invalid expression...")

    try:
        calculator.execute("10 +")

        raise AssertionError(
            "Invalid expression should have failed."
        )

    except ValueError:
        print("✅ Invalid expression correctly rejected.")

    print("\nTesting empty expression...")

    try:
        calculator.execute("")

        raise AssertionError(
            "Empty expression should have failed."
        )

    except ValueError:
        print("✅ Empty expression correctly rejected.")

    print("\nTesting unsafe expression...")

    try:
        calculator.execute(
            "__import__('os').system('dir')"
        )

        raise AssertionError(
            "Unsafe expression should have failed."
        )

    except ValueError:
        print("✅ Unsafe expression correctly rejected.")

    print("\n" + "=" * 60)
    print("✅ CALCULATOR TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    