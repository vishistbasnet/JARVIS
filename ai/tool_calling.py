"""
Gemini tool-calling support for JARVIS.
"""

from __future__ import annotations

from typing import Any

from google import genai
from google.genai import types

from ai.register_tools import register_default_tools
from core.router import ToolRouter

from ai.prompts import JARVIS_SYSTEM_PROMPT
from ai.tool_registry import ToolRegistry
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

        # --------------------------------------------------
        # Tool registry
        # --------------------------------------------------

        self.registry = ToolRegistry()
        register_default_tools(self.registry)
        self.router = ToolRouter(self.registry)

        # --------------------------------------------------
        # Calculator declaration
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Web search declaration
        # --------------------------------------------------

        self.web_search_declaration = (
            types.FunctionDeclaration(
                name="web_search",
                description=(
                    "Search the internet for current or "
                    "up-to-date information. Use this tool "
                    "when the user asks about recent events, "
                    "latest news, current information, "
                    "or information that may have changed "
                    "over time."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "The search query to send "
                                "to the internet."
                            ),
                        },
                        "max_results": {
                            "type": "integer",
                            "description": (
                                "Maximum number of search "
                                "results to return."
                            ),
                            "minimum": 1,
                            "maximum": 10,
                        },
                    },
                    "required": ["query"],
                },
            )
        )
        # --------------------------------------------------
        # Application launcher declaration
        # --------------------------------------------------

        self.app_launcher_declaration = (
            types.FunctionDeclaration(
                name="app_launcher",
                description=(
                    "Open a supported Windows application. "
                    "Use this when the user asks to open, "
                    "launch, or start an application."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "application": {
                            "type": "string",
                            "description": (
                                "The application to open, "
                                "such as Notepad, Calculator, "
                                "File Explorer, Command Prompt, "
                                "or PowerShell."
                            ),
                        }
                    },
                    "required": ["application"],
                },
            )
        )

        # --------------------------------------------------
        # Website launcher declaration
        # --------------------------------------------------

        self.website_launcher_declaration = (
            types.FunctionDeclaration(
                name="website_launcher",
                description=(
                    "Open a supported website in the default "
                    "browser. Use this when the user asks "
                    "to open a website or web service."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "website": {
                            "type": "string",
                            "description": (
                                "The website to open, such as "
                                "Google, YouTube, GitHub, "
                                "LinkedIn, or Gmail."
                            ),
                        }
                    },
                    "required": ["website"],
                },
            )
        )

        # --------------------------------------------------
        # File and folder launcher declaration
        # --------------------------------------------------

        self.file_launcher_declaration = (
            types.FunctionDeclaration(
                name="file_launcher",
                description=(
                    "Open a file or folder on the Windows "
                    "computer. Use this when the user asks "
                    "to open Downloads, Documents, Desktop, "
                    "Pictures, Music, Videos, or a known path."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                "The file, folder, or known "
                                "folder name to open."
                            ),
                        }
                    },
                    "required": ["path"],
                },
            )
        )

        # --------------------------------------------------
        # System control declaration
        # --------------------------------------------------

        self.system_control_declaration = (
            types.FunctionDeclaration(
                name="system_control",
                description=(
                    "Perform a Windows system action such as "
                    "locking or putting the computer to sleep. "
                    "Shutdown and restart require explicit "
                    "confirmation."
                ),
                parameters_json_schema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": (
                                "System action: lock, sleep, "
                                "shutdown, or restart."
                            ),
                            "enum": [
                                "lock",
                                "sleep",
                                "shutdown",
                                "restart",
                            ],
                        },
                        "confirm": {
                            "type": "boolean",
                            "description": (
                                "Must be true to authorize "
                                "shutdown or restart. "
                                "Normally leave false."
                            ),
                        },
                    },
                    "required": ["action"],
                },
            )
        )
        # --------------------------------------------------
        # Gemini tools
        # --------------------------------------------------

        self.calculator_tool = types.Tool(
            function_declarations=[
                self.calculator_declaration
            ]
        )

        self.web_search_tool = types.Tool(
            function_declarations=[
                self.web_search_declaration
            ]
        )

        self.app_launcher_tool = types.Tool(
            function_declarations=[
                self.app_launcher_declaration
            ]
        )

        self.website_launcher_tool = types.Tool(
            function_declarations=[
                self.website_launcher_declaration
            ]
        )

        self.file_launcher_tool = types.Tool(
            function_declarations=[
                self.file_launcher_declaration
            ]
        )

        self.system_control_tool = types.Tool(
            function_declarations=[
                self.system_control_declaration
            ]
        )

        self.gemini_tools = [
            self.calculator_tool,
            self.web_search_tool,
            self.app_launcher_tool,
            self.website_launcher_tool,
            self.file_launcher_tool,
            self.system_control_tool,
        ]

        logger.info(
            "Gemini tool caller initialized with model: %s",
            self.model,
        )

        logger.info(
            "Registered Gemini tools: %s",
            self.registry.list_tools(),
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
                    + "\n\n"
                    + "Use the web_search tool whenever "
                    "the user asks for current, recent, "
                    "latest, live, or time-sensitive "
                    "information. Do not rely on your "
                    "internal knowledge when the answer "
                    "may have changed over time."
                    + "\n\n"
                    + "Use the app_launcher tool when the "
                    "user asks to open or launch a supported "
                    "Windows application."
                    + "\n\n"
                    + "Use the website_launcher tool when "
                    "the user asks to open a supported website "
                    "or web service."
                    + "\n\n"
                    + "Use the file_launcher tool when the "
                    "user asks to open a file, folder, or known "
                    "Windows user folder."
                    + "\n\n"
                    + "Use the system_control tool for Windows "
                    "system actions such as locking or sleeping "
                    "the computer. Never set confirm=true for "
                    "shutdown or restart unless the user has "
                    "explicitly confirmed that action."
                ),
                tools=self.gemini_tools,
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

        result = self.router.execute(function_call.name, arguments)

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

            # Keep Gemini's original model response
            # unchanged. This preserves the Gemini 3
            # thought signature.
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