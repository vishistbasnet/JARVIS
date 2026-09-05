"""
Test JARVIS voice pipeline with tool calling.

This test uses the real microphone and speaker.
"""

from core.assistant import Assistant


def main() -> None:
    print("=" * 60)
    print("JARVIS VOICE TOOL INTEGRATION TEST")
    print("=" * 60)

    assistant = Assistant()

    print("\nAssistant initialized successfully.")

    print("\nSpeak one of these commands:")
    print("1. Open Notepad")
    print("2. Open YouTube")
    print("3. Open my Downloads folder")
    print("4. Calculate 25 times 4")
    print("5. Search the web for the latest AI news")

    print("\nListening...")

    response = assistant.process_once(duration=5.0)

    print("\nJARVIS response:")
    print(response)

    if response:
        print("\nVOICE TOOL INTEGRATION TEST PASSED")
    else:
        print("\nNo response was generated.")


if __name__ == "__main__":
    main()