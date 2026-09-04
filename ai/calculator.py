"""
Calculator tool for JARVIS.

Provides safe arithmetic expression evaluation.
"""

from __future__ import annotations

import ast
import operator
from typing import Any

from ai.tools import Tool


class CalculatorTool(Tool):
    """Safely evaluate basic mathematical expressions."""

    name = "calculator"
    description = (
        "Performs basic arithmetic calculations such as "
        "addition, subtraction, multiplication, division, "
        "and parentheses."
    )

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def execute(
        self,
        expression: str,
        **kwargs: Any,
    ) -> float | int:
        """Evaluate a mathematical expression safely."""

        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        expression = expression.strip()

        if not expression:
            raise ValueError("Expression cannot be empty.")

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )
        except SyntaxError as exc:
            raise ValueError(
                "Invalid mathematical expression."
            ) from exc

        return self._evaluate(tree.body)

    def _evaluate(self, node: ast.AST) -> float | int:
        """Recursively evaluate an allowed AST node."""

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )

        if isinstance(node, ast.BinOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError(
                    "Unsupported mathematical operation."
                )

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError(
                    "Unsupported unary operation."
                )

            operand = self._evaluate(node.operand)

            return operation(operand)

        raise ValueError(
            "Only basic arithmetic expressions are allowed."
        )