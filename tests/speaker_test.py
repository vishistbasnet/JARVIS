"""
Manual text-to-speech test.

Run with:

    python -m tests.speaker_test
"""

from speech.speaker import SpeechSpeaker


def main() -> None:
    print("=" * 60)
    print("              JARVIS SPEAKER TEST")
    print("=" * 60)

    speaker = SpeechSpeaker()

    print("\n🔊 JARVIS is going to speak...")

    speaker.speak(
        "Hello. I am JARVIS. "
        "My text to speech system is working successfully."
    )

    print("\n✅ Text-to-speech test completed.")


if __name__ == "__main__":
    main()