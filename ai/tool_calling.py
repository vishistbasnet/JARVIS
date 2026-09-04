"""
Gemini tool-calling support for JARVIS.
"""

from __future__ import annotations

from typing import Any

from google import genai
from google.genai import types

from ai.calculator import CalculatorTool
from ai.tool_registry import ToolRegistry
from ai.prompts import JARVIS_SYSTEM_PROMPT
from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


class GeminiToolCaller:
    """Handle Gemini requests that may require tools."""

    def __init__(self) -> None:
        settings.require_llm_key()

        self.client = genai.Client(
            api_key=settings.llm_api_key
        )

        self.model = settings.llm_model

        self.registry = ToolRegistry()

        self.registry.register(
            CalculatorTool()
        )

        self.calculator_declaration = (
            types.FunctionDeclaration(
                name="calculator",
                description=(
                    "Perform a mathematical calculation. "
                    "Use this tool when the user asks for "
                    "arithmetic or a mathematical expression."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": (
                                "The mathematical expression "
                                "to calculate, for example "
                                "'25 * 4'."
                            ),
                        }
                    },
                    "required": ["expression"],
                },
            )
        )

        self.calculator_tool = types.Tool(
            function_declarations=[
                self.calculator_declaration
            ]
        )

        logger.info(
            "Gemini tool caller initialized with model: %s",
            self.model,
        )

    def request_tool_call(
        self,
        message: str,
    ) -> tuple[
        types.GenerateContentResponse,
        types.FunctionCall | None,
    ]:
        """
        Ask Gemini whether a tool should be called.
        """

        if not message.strip():
            raise ValueError(
                "Message cannot be empty."
            )

        logger.info(
            "Asking Gemini to determine tool usage."
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=message.strip(),
            config=types.GenerateContentConfig(
                system_instruction=(
                    JARVIS_SYSTEM_PROMPT
                    + "\n\n"
                    + "Use the calculator tool whenever "
                    "the user asks you to perform arithmetic. "
                    "Do not calculate arithmetic yourself "
                    "when the calculator tool is available."
                ),
                tools=[
                    self.calculator_tool
                ],
            ),
        )

        function_calls = response.function_calls

        if not function_calls:
            logger.info(
                "Gemini did not request a tool."
            )

            return response, None

        function_call = function_calls[0]

        logger.info(
            "Gemini requested tool: %s",
            function_call.name,
        )

        logger.info(
            "Tool arguments: %s",
            function_call.args,
        )

        return response, function_call

    def execute_tool_call(
        self,
        function_call: types.FunctionCall,
    ) -> Any:
        """
        Execute a Gemini function call through the registry.
        """

        if not function_call.name:
            raise ValueError(
                "Function call has no tool name."
            )

        arguments = dict(
            function_call.args or {}
        )

        logger.info(
            "Executing Gemini tool call: %s",
            function_call.name,
        )

        tool = self.registry.get(
            function_call.name
        )

        result = tool.execute(
            **arguments
        )

        logger.info(
            "Tool call completed: %s",
            result,
        )

        return result

    def generate_final_response(
        self,
        message: str,
        response: types.GenerateContentResponse,
        tool_result: Any,
    ) -> str:
        """
        Ask Gemini to generate the final response using
        the executed tool result.
        """

        logger.info(
            "Sending tool result back to Gemini."
        )

        model_content = response.candidates[0].content

        function_call = None

        for part in model_content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        if function_call is None:
            raise RuntimeError(
                "No function call found in Gemini response."
            )

        tool_response = types.Part.from_function_response(
            name=function_call.name,
            response={
                "result": tool_result,
            },
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message
                    )
                ],
            ),

            # IMPORTANT:
            # Keep Gemini's original model response unchanged.
            # This preserves the Gemini 3 thought signature.
            model_content,

            # Function responses use role="user"
            # with the GenerateContent API.
            types.Content(
                role="user",
                parts=[
                    tool_response
                ],
            ),
        ]

        final_response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=JARVIS_SYSTEM_PROMPT
            ),
        )

        if not final_response.text:
            raise RuntimeError(
                "Gemini returned an empty final response."
            )

        logger.info(
            "Final Gemini response received."
        )

        return final_response.text.strip()