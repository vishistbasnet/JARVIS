"""
Manual integration test for the JARVIS LLM provider.
"""

from ai.llm import create_llm_provider


def main() -> None:
    print("=" * 60)
    print("              JARVIS LLM TEST")
    print("=" * 60)

    provider = create_llm_provider()

    print("\n🧠 Sending message to JARVIS...\n")

    response = provider.chat(
        "Hello JARVIS. Introduce yourself in one short sentence."
    )

    print("JARVIS:")
    print(response)

    print("\n" + "=" * 60)
    print("✅ LLM test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()