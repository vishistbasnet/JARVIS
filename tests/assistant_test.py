"""
Manual integration test for the complete JARVIS voice pipeline.
"""

from core.assistant import Assistant


def main() -> None:
    print("=" * 60)
    print("             JARVIS ASSISTANT TEST")
    print("=" * 60)

    print("\nInitializing JARVIS...\n")

    assistant = Assistant()

    print("JARVIS is ready.")
    print("\nPress ENTER when you are ready to speak...")

    input()

    print("\n🎤 Listening...")
    print("🗣️ Speak now!\n")

    response = assistant.process_once(duration=5.0)

    if response:
        print("\n" + "-" * 60)
        print("🧠 JARVIS:")
        print(response)
        print("-" * 60)

        print("\n✅ Complete voice pipeline executed successfully.")
    else:
        print("\n⚠️ No speech was recognized.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()