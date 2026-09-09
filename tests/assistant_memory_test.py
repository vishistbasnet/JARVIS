"""
Tests for Assistant memory integration.
"""

from unittest.mock import MagicMock

from core.assistant import Assistant
from core.memory import Memory

def test_assistant_injects_memory_context_into_llm():
    assistant = Assistant.__new__(Assistant)

    assistant.listener = MagicMock()
    assistant.llm = MagicMock()
    assistant.tool_caller = MagicMock()
    assistant.speaker = MagicMock()
    assistant.context = MagicMock()
    assistant.confirmation = MagicMock()
    assistant.memory = MagicMock()

    assistant.listener.listen.return_value.text = (
        "What project am I working on?"
    )

    assistant.context.get_messages.return_value = [
        {
            "role": "user",
            "content": "What project am I working on?",
        }
    ]

    assistant.memory.build_context.return_value = (
        "Relevant memories about the user:\n"
        "- [project] I am working on the JARVIS project."
    )

    assistant.tool_caller.request_tool_call.return_value = (
        MagicMock(),
        None,
    )

    assistant.llm.chat.return_value = (
        "You are working on the JARVIS project."
    )

    response = assistant.process_once()

    assert response == (
        "You are working on the JARVIS project."
    )

    assistant.memory.build_context.assert_called_once_with(
        query="What project am I working on?",
        limit=5,
    )

    assistant.llm.chat.assert_called_once()

    message = assistant.llm.chat.call_args.args[0]

    assert (
        "I am working on the JARVIS project."
        in message
    )

    assert (
        "What project am I working on?"
        in message
    )

def test_assistant_works_without_relevant_memory():
    assistant = Assistant.__new__(Assistant)

    assistant.listener = MagicMock()
    assistant.llm = MagicMock()
    assistant.tool_caller = MagicMock()
    assistant.speaker = MagicMock()
    assistant.context = MagicMock()
    assistant.confirmation = MagicMock()
    assistant.memory = MagicMock()

    assistant.listener.listen.return_value.text = (
        "What is the capital of France?"
    )

    assistant.context.get_messages.return_value = [
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ]

    assistant.memory.build_context.return_value = ""

    assistant.tool_caller.request_tool_call.return_value = (
        MagicMock(),
        None,
    )

    assistant.llm.chat.return_value = "Paris."

    response = assistant.process_once()

    assert response == "Paris."

    assistant.memory.build_context.assert_called_once_with(
        query="What is the capital of France?",
        limit=5,
    )

    assistant.llm.chat.assert_called_once_with(
        "What is the capital of France?",
        history=assistant.context.get_messages.return_value[:-1],
    )

def test_assistant_extracts_memory_when_message_is_candidate():
    assistant = Assistant.__new__(Assistant)
    assistant.listener = MagicMock()
    assistant.llm = MagicMock()
    assistant.tool_caller = MagicMock()
    assistant.speaker = MagicMock()
    assistant.context = MagicMock()
    assistant.confirmation = MagicMock()
    assistant.memory = MagicMock()
    assistant.memory_extractor = MagicMock()

    assistant.listener.listen.return_value.text = (
        "I prefer short answers."
    )

    assistant.context.get_messages.return_value = [
        {
            "role": "user",
            "content": "I prefer short answers.",
        }
    ]

    assistant.memory_extractor.extract.return_value = Memory(
        content="The user prefers short answers.",
        category="preference",
    )

    assistant.memory.remember_from_message.return_value = Memory(
        content="The user prefers short answers.",
        category="preference",
        memory_id=1,
    )

    assistant.tool_caller.request_tool_call.return_value = (
        MagicMock(),
        None,
    )

    assistant.llm.chat.return_value = "Understood."

    response = assistant.process_once()

    assert response == "Understood."

    assistant.memory.remember_from_message.assert_called_once_with(
        user_message="I prefer short answers.",
        extractor=assistant.memory_extractor,
    )

def test_assistant_does_not_extract_memory_for_normal_question():
    assistant = Assistant.__new__(Assistant)
    assistant.listener = MagicMock()
    assistant.llm = MagicMock()
    assistant.tool_caller = MagicMock()
    assistant.speaker = MagicMock()
    assistant.context = MagicMock()
    assistant.confirmation = MagicMock()
    assistant.memory = MagicMock()
    assistant.memory_extractor = MagicMock()

    assistant.listener.listen.return_value.text = (
        "What is the capital of France?"
    )

    assistant.context.get_messages.return_value = [
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ]

    assistant.tool_caller.request_tool_call.return_value = (
        MagicMock(),
        None,
    )

    assistant.llm.chat.return_value = "Paris."

    response = assistant.process_once()

    assert response == "Paris."

    assistant.memory.remember_from_message.assert_not_called()
    assistant.memory_extractor.extract.assert_not_called()

def test_assistant_continues_when_memory_extraction_fails():
    assistant = Assistant.__new__(Assistant)
    assistant.listener = MagicMock()
    assistant.llm = MagicMock()
    assistant.tool_caller = MagicMock()
    assistant.speaker = MagicMock()
    assistant.context = MagicMock()
    assistant.confirmation = MagicMock()
    assistant.memory = MagicMock()
    assistant.memory_extractor = MagicMock()

    assistant.listener.listen.return_value.text = (
        "I prefer concise answers."
    )

    assistant.context.get_messages.return_value = [
        {
            "role": "user",
            "content": "I prefer concise answers.",
        }
    ]

    assistant.memory.remember_from_message.return_value = None

    assistant.tool_caller.request_tool_call.return_value = (
        MagicMock(),
        None,
    )

    assistant.llm.chat.return_value = "Got it."

    response = assistant.process_once()

    assert response == "Got it."

    assistant.memory.remember_from_message.assert_called_once()
    assistant.llm.chat.assert_called_once()