from ai.tool_calling import GeminiToolCaller


def test_tool_selection():
    caller = GeminiToolCaller()

    test_cases = [
        (
            "Open Notepad.",
            "app_launcher",
        ),
        (
            "Open YouTube.",
            "website_launcher",
        ),
        (
            "Open my Downloads folder.",
            "file_launcher",
        ),
        (
            "Lock my computer.",
            "system_control",
        ),
    ]

    for command, expected_tool in test_cases:
        _, function_call = caller.request_tool_call(command)

        assert function_call is not None
        assert function_call.name == expected_tool