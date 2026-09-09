"""
Task planning for JARVIS multi-step tasks.
"""

from __future__ import annotations

import json

from core.task import Task, TaskStep


class TaskPlanner:
    """Create executable task plans using the LLM."""

    def __init__(self, llm, available_actions=None):
        self.llm = llm
        self.available_actions = list(available_actions or [])

    def create_plan(self, goal: str) -> Task:
        if not goal.strip():
            raise ValueError("Goal cannot be empty.")

        available_tools = ", ".join(self.available_actions)

        prompt = f"""
You are the task planner for JARVIS.

Convert the user's goal into a simple ordered execution plan.

User goal:
{goal}

Available JARVIS tools:
{available_tools}

Return ONLY valid JSON in this format:

{{
  "steps": [
    {{
      "action": "tool_name",
      "arguments": {{}}
    }}
  ]
}}

Rules:
- Create only the steps necessary to accomplish the goal.
- Steps must be ordered.
- Use ONLY the available JARVIS tool names listed above.
- Do not invent or rename tool names.
- Do not execute tools.
- Do not add explanations.
"""

        response = self.llm.chat(prompt)

        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Planner returned invalid JSON."
            ) from exc

        steps = []

        for step in data.get("steps", []):
            steps.append(
                TaskStep(
                    action=step["action"],
                    arguments=step.get("arguments", {}),
                )
            )

        return Task(
            goal=goal,
            steps=steps,
        )