from unittest.mock import Mock

from core.assistant import Assistant


def create_assistant_for_test():
    assistant = Assistant.__new__(Assistant)

    assistant.context = Mock()
    assistant.speaker = Mock()

    return assistant


def test_successful_tool_result_has_safe_fallback():
    assistant = create_assistant_for_test()

    tool_result = {
        "status": "success",
        "action": "sleep",
        "message": "Computer entering sleep mode.",
    }

    response = assistant._build_tool_fallback(
        tool_result
    )

    assert response == "Computer entering sleep mode."


def test_successful_tool_without_message_has_generic_fallback():
    assistant = create_assistant_for_test()

    tool_result = {
        "status": "success",
        "action": "calculator",
    }

    response = assistant._build_tool_fallback(
        tool_result
    )

    assert (
        response
        == "The requested action was completed successfully."
    )


def test_failed_tool_result_has_failure_fallback():
    assistant = create_assistant_for_test()

    tool_result = {
        "status": "error",
        "message": "Application could not be opened.",
    }

    response = assistant._build_tool_fallback(
        tool_result
    )

    assert (
        response
        == "I couldn't complete the request. "
        "Application could not be opened."
    )


def test_failed_tool_without_message_has_generic_failure():
    assistant = create_assistant_for_test()

    tool_result = {
        "status": "error",
    }

    response = assistant._build_tool_fallback(
        tool_result
    )

    assert response == "I couldn't complete the requested action."


def test_unknown_tool_status_is_safe():
    assistant = create_assistant_for_test()

    tool_result = {
        "status": "unknown",
    }

    response = assistant._build_tool_fallback(
        tool_result
    )

    assert (
        response
        == "The tool completed with an unexpected result, "
        "and I couldn't generate a final response."
    )