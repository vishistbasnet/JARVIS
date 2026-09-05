import pytest

from ai.calculator import CalculatorTool


@pytest.fixture
def calculator():
    return CalculatorTool()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("10 + 5", 15),
        ("25 * 4", 100),
        ("100 / 5", 20),
        ("(10 + 5) * 2", 30),
        ("2 ** 5", 32),
    ],
)
def test_calculator_operations(calculator, expression, expected):
    assert calculator.execute(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "10 +",
        "__import__('os').system('dir')",
    ],
)
def test_calculator_rejects_invalid_or_unsafe_expressions(
    calculator,
    expression,
):
    with pytest.raises(ValueError):
        calculator.execute(expression)
