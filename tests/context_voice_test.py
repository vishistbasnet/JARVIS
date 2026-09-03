"""
Real two-turn voice test for JARVIS context memory.
"""

from core.assistant import Assistant


def main() -> None:
    print("=" * 60)
    print("       JARVIS TWO-TURN VOICE CONTEXT TEST")
    print("=" * 60)

    assistant = Assistant()

    print("\nTurn 1")
    print("-" * 60)
    print("Say: My name is Vishist.")

    input("\nPress ENTER when ready...")

    response_1 = assistant.process_once(
        duration=5.0
    )

    print("\nJARVIS:")
    print(response_1)

    print("\nTurn 2")
    print("-" * 60)
    print("Say: What is my name?")

    input("\nPress ENTER when ready...")

    response_2 = assistant.process_once(
        duration=5.0
    )

    print("\nJARVIS:")
    print(response_2)

    print("\nStored conversation:")
    print("-" * 60)

    for message in assistant.context.get_messages():
        print(
            f"{message.role.upper()}: "
            f"{message.content}"
        )

    print("\n" + "=" * 60)
    print("✅ TWO-TURN VOICE CONTEXT TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()