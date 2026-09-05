from core.confirmation import ConfirmationManager


def test_shutdown_confirmation():
    manager = ConfirmationManager()

    message = manager.request_confirmation("shutdown")

    assert "confirmation" in message.lower()
    assert manager.pending_action == "shutdown"

    result = manager.process_response("yes")

    assert result["status"] == "confirmed"
    assert result["action"] == "shutdown"
    assert manager.pending_action is None


def test_restart_cancellation():
    manager = ConfirmationManager()

    manager.request_confirmation("restart")

    assert manager.pending_action == "restart"

    result = manager.process_response("no")

    assert result["status"] == "cancelled"
    assert result["action"] == "restart"
    assert manager.pending_action is None


def test_unclear_confirmation_keeps_pending_action():
    manager = ConfirmationManager()

    manager.request_confirmation("shutdown")

    result = manager.process_response("maybe")

    assert result["status"] == "unclear"
    assert result["action"] == "shutdown"
    assert manager.pending_action == "shutdown"


def test_cancel_clears_pending_confirmation():
    manager = ConfirmationManager()

    manager.request_confirmation("shutdown")

    assert manager.pending_action == "shutdown"

    manager.cancel()

    assert manager.pending_action is None


def test_response_without_pending_confirmation():
    manager = ConfirmationManager()

    result = manager.process_response("yes")

    assert result["status"] == "no_pending_confirmation"


def test_only_sensitive_actions_can_request_confirmation():
    manager = ConfirmationManager()

    try:
        manager.request_confirmation("lock")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError for a non-sensitive action."
        )
