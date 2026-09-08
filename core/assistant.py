"""
Main JARVIS assistant.

Coordinates speech recognition, Gemini, tool calling,
safety confirmation, context management, and text-to-speech.
"""

from __future__ import annotations

from ai.llm import create_llm_provider
from ai.tool_calling import GeminiToolCaller
from core.confirmation import ConfirmationManager
from core.context import ContextManager
from core.errors import LLMError, SpeechError
from speech.listener import SpeechListener
from speech.speaker import SpeechSpeaker
from utils.logger import get_logger

logger = get_logger(__name__)


class Assistant:
    """Main JARVIS voice assistant."""

    def __init__(self) -> None:
        logger.info("Initializing JARVIS assistant...")

        self.listener = SpeechListener()
        self.llm = create_llm_provider()
        self.tool_caller = GeminiToolCaller()
        self.speaker = SpeechSpeaker()
        self.context = ContextManager(max_messages=10)
        self.confirmation = ConfirmationManager()

        logger.info("JARVIS assistant initialized successfully.")

    def _speak_safely(self, response: str) -> None:
        """
        Speak a response without allowing TTS failure to
        terminate the assistant.
        """

        try:
            self.speaker.speak(response)

        except Exception as exc:
            logger.exception(
                "Text-to-speech failed. Continuing without audio."
            )

            print()
            print("JARVIS:", response)
            print(
                f"[TTS unavailable: {exc}]"
            )

    def process_once(self, duration: float = 5.0) -> str:
        """Process one complete voice interaction."""

        logger.info("Waiting for user speech...")

        try:
            result = self.listener.listen(duration=duration)

        except SpeechError as exc:
            logger.exception(
                "Speech input failed. Continuing without processing."
            )

            print(f"[Speech unavailable: {exc}]")

            return ""

        user_text = result.text.strip()

        if not user_text:
            logger.warning("No speech was recognized.")
            return ""

        logger.info("User said: %s", user_text)

        self.context.add_user_message(user_text)

        history = self.context.get_messages()

        logger.info(
            "Conversation context contains %d messages.",
            len(history),
        )

        logger.info("Checking whether a tool is required...")

        gemini_response, function_call = (
            self.tool_caller.request_tool_call(user_text)
        )

        if function_call is not None:
            logger.info(
                "Gemini selected tool: %s",
                function_call.name,
            )

            tool_result = self.tool_caller.execute_tool_call(
                function_call
            )

            logger.info("Tool result received.")

            if tool_result.get("status") == "confirmation_required":
                return self._handle_confirmation(
                    function_call=function_call,
                    duration=duration,
                )
            try:
                response = self.tool_caller.generate_final_response(
                    message=user_text,
                    response=gemini_response,
                    tool_result=tool_result,
                )
            except LLMError:
                logger.exception(
                    "Gemini final response failed after tool execution. "
                    "Using local fallback response."
                )

                response = self._build_tool_fallback(
                    tool_result=tool_result,
                )
        else:
            logger.info(
                "No tool required. Using normal LLM response."
            )

            response = self.llm.chat(
                user_text,
                history=history[:-1],
            )

        self.context.add_assistant_message(response)

        logger.info("Speaking JARVIS response...")

        self._speak_safely(response)

        logger.info("Voice interaction completed.")

        return response

    def _build_tool_fallback(
        self,
        tool_result,
    ) -> str:
        """
        Build a safe local response when Gemini cannot generate
        the final response after a tool has already executed.

        The response is based only on the actual tool result.
        """

        status = tool_result.get("status")

        if status == "success":
            message = tool_result.get("message")

            if message:
                return str(message)

            return "The requested action was completed successfully."

        if status == "error":
            message = tool_result.get("message")

            if message:
                return f"I couldn't complete the request. {message}"

            return "I couldn't complete the requested action."

        return (
            "The tool completed with an unexpected result, "
            "and I couldn't generate a final response."
        )

    def _handle_confirmation(
        self,
        function_call,
        duration: float,
    ) -> str:
        """Handle confirmation for a sensitive action."""

        arguments = function_call.args or {}

        action = str(
            arguments.get("action", "")
        ).strip().lower()

        if not action:
            raise ValueError(
                "Sensitive tool call did not provide an action."
            )

        logger.info(
            "Confirmation required for action: %s",
            action,
        )

        confirmation_message = (
            self.confirmation.request_confirmation(action)
        )

        self._speak_safely(confirmation_message)

        logger.info(
            "Waiting for confirmation response..."
        )

        result = self.listener.listen(
            duration=duration
        )

        confirmation_text = result.text.strip()

        logger.info(
            "Confirmation response: %s",
            confirmation_text,
        )

        confirmation_result = (
            self.confirmation.process_response(
                confirmation_text
            )
        )

        logger.info(
            "Confirmation result: %s",
            confirmation_result,
        )

        status = confirmation_result["status"]

        if status == "cancelled":
            response = (
                f"{action.capitalize()} cancelled."
            )

            self.context.add_assistant_message(response)
            self._speak_safely(response)

            return response

        if status == "unclear":
            response = confirmation_result["message"]

            self.context.add_assistant_message(response)
            self._speak_safely(response)

            return response

        if status != "confirmed":
            raise RuntimeError(
                f"Unexpected confirmation status: {status}"
            )

        logger.info(
            "Confirmation accepted for action: %s",
            action,
        )

        return self._execute_confirmed_action(
            action=action,
        )

    def _execute_confirmed_action(
        self,
        action: str,
    ) -> str:
        """
        Execute an action after explicit confirmation.

        Gemini is not consulted again. The system-control
        tool is executed directly with explicit confirmation
        """

        logger.warning(
            "Executing confirmed sensitive action: %s",
            action,
        )

        tool = self.tool_caller.registry.get(
            "system_control"
        )

        tool_result = tool.execute(
            action=action,
            confirm=True,
        )

        logger.info(
            "Confirmed system action result: %s",
            tool_result,
        )

        if tool_result.get("status") != "success":
            response = tool_result.get(
                "message",
                f"Unable to execute {action}.",
            )

            self.context.add_assistant_message(response)
            self._speak_safely(response)

            return response

        response = tool_result.get(
            "message",
            f"{action.capitalize()} initiated.",
        )

        self.context.add_assistant_message(response)

        self._speak_safely(response)

        return response
