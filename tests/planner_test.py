from core.planner import TaskPlanner
from core.task import TaskStatus
from unittest.mock import Mock

class FakeLLM:
    def __init__(self, response):
        self.response = response
        self.last_prompt = None

    def chat(self, prompt):
        self.last_prompt = prompt
        return self.response 

def test_planner_creates_task():
    llm = FakeLLM(
        '{"goal":"Search AI news","steps":[{"action":"web_search","arguments":{"query":"AI news"}}]}'
    )

    planner = TaskPlanner(llm)
    task = planner.create_plan("Search AI news")

    assert task.goal == "Search AI news"
    assert len(task.steps) == 1
    assert task.steps[0].action == "web_search"
    assert task.steps[0].arguments["query"] == "AI news"
    assert task.status == TaskStatus.PENDING


def test_planner_creates_multiple_steps():
    llm = FakeLLM(
        """
        {
            "goal": "Search and summarize AI news",
            "steps": [
                {
                    "action": "web_search",
                    "arguments": {"query": "AI news"}
                },
                {
                    "action": "summarize",
                    "arguments": {}
                }
            ]
        }
        """
    )

    planner = TaskPlanner(llm)
    task = planner.create_plan("Search and summarize AI news")

    assert len(task.steps) == 2
    assert task.steps[0].action == "web_search"
    assert task.steps[1].action == "summarize"


def test_planner_prompt_contains_goal():
    llm = FakeLLM(
        '{"goal":"Open YouTube","steps":[{"action":"open_application","arguments":{"application":"youtube"}}]}'
    )

    planner = TaskPlanner(llm)
    planner.create_plan("Open YouTube")

    assert "Open YouTube" in llm.last_prompt

def test_planner_prompt_contains_available_actions():
    llm = Mock()
    llm.chat.return_value = '{"steps": []}'

    planner = TaskPlanner(
        llm=llm,
        available_actions=["calculator", "web_search"],
    )

    planner.create_plan("Calculate 10 + 5")

    prompt = llm.chat.call_args[0][0]

    assert "calculator" in prompt
    assert "web_search" in prompt
    assert "Do not invent or rename tool names." in prompt