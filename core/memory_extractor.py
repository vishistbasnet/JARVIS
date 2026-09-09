"""
Automatic memory extraction for JARVIS.
"""

from __future__ import annotations

import json

from ai.llm import LLMProvider
from core.memory import Memory


MEMORY_EXTRACTION_PROMPT = """
You are a memory extraction component for a personal AI assistant.

Analyze the user's message and determine whether it contains information
that is useful to remember for future conversations.

Only extract stable, user-specific information such as:
- preferences
- projects
- goals
- personal facts
- important recurring information

Do NOT extract:
- temporary requests
- questions
- commands
- greetings
- general knowledge
- information about other people
- sensitive information
- information that is only relevant to the current conversation

Return ONLY valid JSON in exactly this format:

{
  "should_remember": true,
  "content": "short memory statement",
  "category": "preference"
}

If nothing should be remembered, return:

{
  "should_remember": false,
  "content": "",
  "category": "general"
}

Allowed categories:
- preference
- project
- goal
- personal
- general

User message:
""".strip()


class MemoryExtractor:
    """Extract potentially useful memories from user messages."""

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def extract(self, user_message: str) -> Memory | None:
        """Extract one memory from a user message."""

        if not user_message.strip():
            return None

        prompt = (
            f"{MEMORY_EXTRACTION_PROMPT}\n\n"
            f"{user_message.strip()}"
        )

        response = self.llm.chat(prompt)

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            return None

        if not data.get("should_remember", False):
            return None

        content = str(
            data.get("content", "")
        ).strip()

        category = str(
            data.get("category", "general")
        ).strip().lower()

        if not content:
            return None

        allowed_categories = {
            "preference",
            "project",
            "goal",
            "personal",
            "general",
        }

        if category not in allowed_categories:
            category = "general"

        return Memory(
            content=content,
            category=category,
        )