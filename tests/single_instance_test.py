from unittest.mock import MagicMock, patch

import pytest

from utils.single_instance import (
    ERROR_ALREADY_EXISTS,
    SingleInstanceError,
    SingleInstanceLock,
)


def _mock_ctypes(create_returns, last_error):
    """
    Build a fake `ctypes` module with just enough surface for
    SingleInstanceLock: a `.windll.kernel32` with CreateMutexW,
    GetLastError, and CloseHandle.

    We patch the whole `ctypes` reference (rather than
    `ctypes.windll`) because `windll` only exists on real Windows
    Python builds -- patching a nonexistent attribute raises
    AttributeError on Linux/macOS, which would make these tests
    fail outside Windows even though the logic under test has
    nothing OS-specific about it.
    """

    kernel32 = MagicMock()
    kernel32.CreateMutexW.return_value = create_returns
    kernel32.GetLastError.return_value = last_error

    fake_ctypes = MagicMock()
    fake_ctypes.windll.kernel32 = kernel32

    return fake_ctypes, kernel32


def test_acquire_succeeds_when_no_other_instance():
    fake_ctypes, kernel32 = _mock_ctypes(create_returns=12345, last_error=0)

    with patch("utils.single_instance.ctypes", fake_ctypes):
        lock = SingleInstanceLock()
        lock.acquire()

    kernel32.CreateMutexW.assert_called_once()
    kernel32.CloseHandle.assert_not_called()


def test_acquire_raises_when_instance_already_running():
    fake_ctypes, kernel32 = _mock_ctypes(
        create_returns=12345,
        last_error=ERROR_ALREADY_EXISTS,
    )

    with patch("utils.single_instance.ctypes", fake_ctypes):
        lock = SingleInstanceLock()

        with pytest.raises(SingleInstanceError):
            lock.acquire()

    # The duplicate handle must be closed, not leaked.
    kernel32.CloseHandle.assert_called_once_with(12345)


def test_acquire_raises_if_mutex_creation_fails():
    fake_ctypes, _kernel32 = _mock_ctypes(create_returns=0, last_error=0)

    with patch("utils.single_instance.ctypes", fake_ctypes):
        lock = SingleInstanceLock()

        with pytest.raises(SingleInstanceError):
            lock.acquire()


def test_release_closes_handle_once():
    fake_ctypes, kernel32 = _mock_ctypes(create_returns=999, last_error=0)

    with patch("utils.single_instance.ctypes", fake_ctypes):
        lock = SingleInstanceLock()
        lock.acquire()
        lock.release()
        lock.release()  # Calling twice must be a no-op, not an error.

    kernel32.CloseHandle.assert_called_once_with(999)


def test_context_manager_acquires_and_releases():
    fake_ctypes, kernel32 = _mock_ctypes(create_returns=555, last_error=0)

    with patch("utils.single_instance.ctypes", fake_ctypes):
        with SingleInstanceLock():
            kernel32.CreateMutexW.assert_called_once()

    kernel32.CloseHandle.assert_called_once_with(555)