from __future__ import annotations

from ai.llm import create_llm_provider
from ai.tool_calling import GeminiToolCaller
from core.context import ContextManager
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

        # Short-term conversation memory.
        self.context = ContextManager(
            max_messages=10
        )

        logger.info(
            "JARVIS assistant initialized successfully."
        )

    def process_once(
        self,
        duration: float = 5.0,
    ) -> str:
        """Process one complete voice interaction."""

        logger.info(
            "Waiting for user speech..."
        )

        result = self.listener.listen(
            duration=duration
        )

        user_text = result.text.strip()

        if not user_text:
            logger.warning(
                "No speech was recognized."
            )
            return ""

        logger.info(
            "User said: %s",
            user_text,
        )

        # Store user message in short-term memory.
        self.context.add_user_message(
            user_text
        )

        history = self.context.get_messages()

        logger.info(
            "Conversation context contains %d messages.",
            len(history),
        )

        # --------------------------------------------------
        # STEP 1: Ask Gemini whether a tool is required.
        # --------------------------------------------------

        logger.info(
            "Checking whether a tool is required..."
        )

        if isinstance(
            self.tool_caller,
            GeminiToolCaller,
        ):
            gemini_response, function_call = (
                self.tool_caller.request_tool_call(
                    user_text
                )
            )

            # --------------------------------------------------
            # STEP 2: Tool required.
            # --------------------------------------------------

            if function_call is not None:

                logger.info(
                    "Gemini selected tool: %s",
                    function_call.name,
                )

                tool_result = (
                    self.tool_caller.execute_tool_call(
                        function_call
                    )
                )

                logger.info(
                    "Tool result: %s",
                    tool_result,
                )

                # --------------------------------------------------
                # STEP 3: Send tool result back to Gemini.
                # --------------------------------------------------

                response = (
                    self.tool_caller.generate_final_response(
                        message=user_text,
                        response=gemini_response,
                        tool_result=tool_result,
                    )
                )

            # --------------------------------------------------
            # STEP 2: No tool required.
            # --------------------------------------------------

            else:

                logger.info(
                    "No tool required. Using normal LLM response."
                )

                response = self.llm.chat(
                    user_text,
                    history=history[:-1],
                )

        else:
            # Fallback for future non-Gemini providers.
            response = self.llm.chat(
                user_text,
                history=history[:-1],
            )

        # Store assistant response in memory.
        self.context.add_assistant_message(
            response
        )

        logger.info(
            "Speaking JARVIS response..."
        )

        self.speaker.speak(
            response
        )

        logger.info(
            "Voice interaction completed."
        )

        return response