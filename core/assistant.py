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
from core.errors import LLMError, SpeechError, TTSError
from core.memory_manager import MemoryManager
from core.memory_extractor import MemoryExtractor
from core.plan_validator import PlanValidator
from core.planner import TaskPlanner
from core.task_executor import TaskExecutor
from core.memory_trigger import should_consider_memory
from core.conversation_state import ConversationStateManager
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

        self.memory = MemoryManager()
        self.memory_extractor = MemoryExtractor(
            llm=self.llm,
        )

        # Confirmation must exist before TaskExecutor.
        self.confirmation = ConfirmationManager()

        self.conversation_state = ConversationStateManager()

        # Planning and execution.
        self.planner = TaskPlanner(
            llm=self.llm,
            available_actions=self.tool_caller.registry.list_tools(),
        )

        self.plan_validator = PlanValidator(
            allowed_actions=set(self.tool_caller.registry.list_tools())
        )

        self.task_executor = TaskExecutor(
            tool_router=self.tool_caller.router,
            confirmation_manager=self.confirmation,
            confirmation_callback=self._confirm_planned_action,
        )

        logger.info("JARVIS assistant initialized successfully.")

    def _speak_safely(self, response: str) -> None:
        """
        Speak a response without allowing TTS failure to
        terminate the assistant.

        TTS is an optional output channel. If speech fails,
        the response is still printed so the assistant can
        continue.
        """

        try:
            self.speaker.speak(response)

        except TTSError as exc:
            logger.exception(
                "Text-to-speech failed. Continuing without audio."
            )

            print()
            print("JARVIS:", response)
            print(
                f"[TTS unavailable: {exc}]"
            )

        except Exception as exc:
            logger.exception(
                "Unexpected TTS error. Continuing without audio."
            )
            print()
            print("JARVIS:", response)
            print(f"[TTS unavailable: {exc}]")

    def process_once(self, duration: float = 5.0) -> str:
        if not hasattr(self, "conversation_state"):
            self.conversation_state = ConversationStateManager()

        self.conversation_state.start()
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

        if should_consider_memory(user_text):
            logger.info("Message may contain a memory. Extracting...")
        
            memory = self.memory.remember_from_message(
                user_message=user_text,
                extractor=self.memory_extractor,
            )
        
            if memory is not None:
                logger.info(
                    "Memory stored: [%s] %s",
                    memory.category,
                    memory.content,
                )
            else:
                logger.info("No memory extracted.")

        history = self.context.get_messages()

        memory_context = self.memory.build_context(
            query=user_text,
            limit=5,
        )

        if memory_context:
            logger.info("Relevant memory context found.")
        else:
            logger.info("No relevant memories found.")

        logger.info(
            "Conversation context contains %d messages.",
            len(history),
        )
        if self._should_create_plan(user_text):
            response = self._process_planned_task(user_text)

            self.context.add_assistant_message(response)

            logger.info("Speaking JARVIS response...")
            self._speak_safely(response)

            logger.info("Planned voice interaction completed.")

            return response

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

            message = user_text

            if memory_context:
                message = (
                    f"{memory_context}\n\n"
                    f"User request:\n{user_text}"
                )

            response = self.llm.chat(
                message,
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

        try:
            result = self.listener.listen(
                duration=duration,
            )

        except SpeechError as exc:
            logger.exception(
                "Speech recognition failed while waiting for confirmation."
            )

            print()
            print("JARVIS: I couldn't hear your confirmation.")
            print(f"[Speech unavailable: {exc}]")

            return False
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

    def _should_create_plan(self, message: str) -> bool:
        """Determine whether a request is likely multi-step."""

        text = message.lower().strip()

        planning_phrases = (
            " and then ",
            " then ",
            "after that",
            "followed by",
            "first ",
            "finally ",
            "step by step",
            "and open",
            "and search",
            "and summarize",
            "and tell me",
            "and send",
        )

        return any(
            phrase in f" {text} "
            for phrase in planning_phrases
        )

    def _process_planned_task(self, user_text: str) -> str:
        """Create, validate, and execute a multi-step task."""

        logger.info(
            "Multi-step request detected. Creating task plan..."
        )

        task = self.planner.create_plan(user_text)

        logger.info(
            "Task plan created with %d steps.",
            len(task.steps),
        )

        self.plan_validator.validate(task)

        logger.info("Task plan validated successfully.")

        try:
            task = self.task_executor.execute(task)

        except Exception as exc:
            logger.exception(
                "Planned task execution failed."
            )

            return (
                "I couldn't complete the multi-step task. "
                f"{exc}"
            )

        completed_steps = sum(
            1
            for step in task.steps
            if step.status.value == "completed"
        )

        return (
            f"Task completed successfully. "
            f"{completed_steps} step(s) completed."
        )

    def _confirm_planned_action(self, action: str) -> bool:
        """Request voice confirmation for a dangerous planned action."""

        logger.info(
            "Planned task requires confirmation for action: %s",
            action,
        )

        prompt = self.confirmation.request_confirmation(action)
        self._speak_safely(prompt)

        try:
            response = self.listener.listen()
        except Exception:
            logger.exception(
                "Failed to capture confirmation response."
            )
            self.confirmation.cancel()
            return False

        result = self.confirmation.process_response(response)

        if result == "confirmed":
            logger.info(
                "User confirmed planned action: %s",
                action,
            )
            return True

        if result == "cancelled":
            logger.info(
                "User cancelled planned action: %s",
                action,
            )
            return False

        logger.info(
            "Confirmation response was unclear for action: %s",
            action,
        )

        self.confirmation.cancel()
        return False