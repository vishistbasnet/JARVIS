"""
Manual speech recognition test.

Run with:

    python tests/speech_test.py
"""

from speech.listener import SpeechListener


def main() -> None:
    print("=" * 60)
    print("              JARVIS SPEECH TEST")
    print("=" * 60)

    print("\nLoading speech recognition system...")

    listener = SpeechListener()

    print("\nWhisper model will be loaded when recording starts.")
    print("The first run may take some time because the model")
    print("needs to be downloaded.\n")

    input("Press ENTER when you are ready to speak...")

    print("\n🎤 Listening...")
    print("🗣️  Speak now!")

    result = listener.listen(duration=5.0)

    print("\n" + "-" * 60)
    print(f"📝 Recognized: {result.text or '[nothing detected]'}")
    print("-" * 60)

    if result.text:
        print("\n✅ Speech recognition successful.")
    else:
        print("\n⚠️ No speech was detected.")


if __name__ == "__main__":
    main()