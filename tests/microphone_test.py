import sounddevice as sd


def main():
    print("=" * 50)
    print("JARVIS MICROPHONE TEST")
    print("=" * 50)

    print("\nAvailable audio devices:\n")
    print(sd.query_devices())

    print("\nDefault input device:")
    print(sd.query_devices(sd.default.device[0]))

    print("\nMicrophone configuration:")
    print(f"Sample rate: {sd.default.samplerate}")
    print(f"Input device: {sd.default.device[0]}")

    print("\nMicrophone detection successful.")


if __name__ == "__main__":
    main()
    