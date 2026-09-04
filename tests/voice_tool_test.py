"""
Real voice integration test for JARVIS tool calling.

Pipeline:

Microphone
    ↓
Speech Recognition
    ↓
Gemini Tool Calling
    ↓
Calculator
    ↓
Gemini Final Response
    ↓
Text-to-Speech
"""

from ai.tool_calling import GeminiToolCaller
from speech.listener import SpeechListener
from speech.speaker import SpeechSpeaker


def main() -> None:
    print("=" * 60)
    print("          JARVIS VOICE TOOL INTEGRATION TEST")
    print("=" * 60)

    listener = SpeechListener()
    caller = GeminiToolCaller()
    speaker = SpeechSpeaker()

    print("\nJARVIS is ready.")
    print(
        "\nSay something like:"
    )
    print(
        '"What is 25 multiplied by 40?"'
    )

    print("\n" + "-" * 60)

    # --------------------------------------------------
    # Step 1: Listen
    # --------------------------------------------------

    print("\nStep 1: Listening...")

    result = listener.listen(
        duration=5.0
    )

    user_text = result.text.strip()

    print(
        f"Recognized: {user_text}"
    )

    if not user_text:
        print(
            "\n❌ No speech was recognized."
        )
        return

    # --------------------------------------------------
    # Step 2: Ask Gemini for tool decision
    # --------------------------------------------------

    print(
        "\nStep 2: Asking Gemini for tool decision..."
    )

    gemini_response, function_call = (
        caller.request_tool_call(
            user_text
        )
    )

    if function_call is None:
        print(
            "\nNo tool was requested."
        )

        print(
            "\nGenerating normal response..."
        )

        response = caller.client.models.generate_content(
            model=caller.model,
            contents=user_text,
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        final_response = response.text.strip()

    else:
        print(
            f"\nTool selected: "
            f"{function_call.name}"
        )

        print(
            f"Arguments: "
            f"{function_call.args}"
        )

        # --------------------------------------------------
        # Step 3: Execute tool
        # --------------------------------------------------

        print(
            "\nStep 3: Executing tool..."
        )

        tool_result = caller.execute_tool_call(
            function_call
        )

        print(
            f"Tool result: {tool_result}"
        )

        # --------------------------------------------------
        # Step 4: Generate final response
        # --------------------------------------------------

        print(
            "\nStep 4: Generating final response..."
        )

        final_response = (
            caller.generate_final_response(
                message=user_text,
                response=gemini_response,
                tool_result=tool_result,
            )
        )

    # --------------------------------------------------
    # Step 5: Speak
    # --------------------------------------------------

    print(
        "\nJARVIS:"
    )

    print(
        final_response
    )

    print(
        "\nStep 5: Speaking response..."
    )

    speaker.speak(
        final_response
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "✅ VOICE TOOL INTEGRATION TEST PASSED"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()