"""
Integration test for JARVIS conversation context.
"""

from ai.llm import create_llm_provider
from core.context import ContextManager


def main() -> None:
    print("=" * 60)
    print("        JARVIS CONTEXT INTEGRATION TEST")
    print("=" * 60)

    context = ContextManager(
        max_messages=10
    )

    llm = create_llm_provider()

    # First turn.
    user_message = "My name is Vishist."

    print("\nUSER:")
    print(user_message)

    context.add_user_message(
        user_message
    )

    response = llm.chat(
        user_message,
        history=context.get_messages()[:-1],
    )

    print("\nJARVIS:")
    print(response)

    context.add_assistant_message(
        response
    )

    # Second turn.
    user_message = "What is my name?"

    print("\nUSER:")
    print(user_message)

    context.add_user_message(
        user_message
    )

    response = llm.chat(
        user_message,
        history=context.get_messages()[:-1],
    )

    print("\nJARVIS:")
    print(response)

    context.add_assistant_message(
        response
    )

    print("\nConversation messages:")
    print(context.count())

    print("\n" + "=" * 60)
    print("✅ CONTEXT INTEGRATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()