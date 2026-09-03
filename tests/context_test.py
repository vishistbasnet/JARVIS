"""
Tests for JARVIS conversation context.
"""

from core.context import ContextManager


def main() -> None:
    print("=" * 60)
    print("             JARVIS CONTEXT TEST")
    print("=" * 60)

    context = ContextManager(max_messages=4)

    print("\nAdding conversation...")

    context.add_user_message(
        "My name is Vishist."
    )

    context.add_assistant_message(
        "Nice to meet you, Vishist."
    )

    context.add_user_message(
        "What can you help me with?"
    )

    context.add_assistant_message(
        "I can help with many tasks."
    )

    print(
        f"Messages stored: {context.count()}"
    )

    print("\nConversation history:")

    for message in context.get_messages():
        print(
            f"{message.role.upper()}: "
            f"{message.content}"
        )

    print("\nTesting context limit...")

    context.add_user_message(
        "Tell me a joke."
    )

    print(
        f"Messages after limit: {context.count()}"
    )

    messages = context.get_messages()

    # Context should not begin with an orphaned
    # assistant response.
    assert messages[0].role == "user"

    # Newest message must always be preserved.
    assert (
        messages[-1].content
        == "Tell me a joke."
    )

    print("✅ Context limit working.")
    print("✅ Conversation turn integrity preserved.")

    print("\nTesting clear()...")

    context.clear()

    assert context.count() == 0

    print("✅ Context cleared successfully.")

    print("\n" + "=" * 60)
    print("✅ CONTEXT TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()