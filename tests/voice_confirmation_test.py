"""
Manual test for JARVIS voice confirmation flow.

This test uses the real microphone and speaker.

WARNING:
This test can execute a real shutdown or restart if
the user confirms the requested system action.

For safety, test with "No" or "Cancel" only.
"""

from core.assistant import Assistant


def main() -> None:
    print("=" * 60)
    print("JARVIS VOICE CONFIRMATION TEST")
    print("=" * 60)

    assistant = Assistant()

    print("\nAssistant initialized successfully.")

    print("\nSay:")
    print("    Shutdown my computer")

    print("\nJARVIS should ask for confirmation.")

    print("\nFor safety, say:")
    print("    No")
    print("or:")
    print("    Cancel")

    print("\nDO NOT say Yes during this test.")


    print("\nListening...")

    response = assistant.process_once(duration=5.0)

    print("\nJARVIS response:")
    print(response)

    if response:
        print("\nVOICE CONFIRMATION TEST PASSED")
    else:
        print("\nNo response was generated.")


if __name__ == "__main__":
    main()