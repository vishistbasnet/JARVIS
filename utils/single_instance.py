"""
Single-instance guard for JARVIS.

Prevents two copies of JARVIS from running at the same time on the
same machine. Two instances competing for the same microphone can
produce interleaved or misattributed speech input, which is
especially dangerous for confirmation prompts on sensitive actions
(shutdown/restart): a "yes" meant for one instance's question could
be picked up as input by the other.

Implemented with a Windows named mutex (via ctypes, already a
dependency of this project through core/system_control.py), so no
extra package is required. The mutex is automatically released by
Windows when the process exits or crashes, so there is no stale
lock-file cleanup to worry about.
"""

from __future__ import annotations

import ctypes

from utils.logger import get_logger

logger = get_logger(__name__)

# A GUID-like name keeps this extremely unlikely to collide with any
# other application's mutex on the system.
_MUTEX_NAME = "Global\\JARVIS_SINGLE_INSTANCE_9F3B2C7E-4B7B-4E2E-9B1E-4C6B7E2F3A11"

ERROR_ALREADY_EXISTS = 183


class SingleInstanceError(RuntimeError):
    """Raised when another instance of JARVIS is already running."""


class SingleInstanceLock:
    """
    Acquire a system-wide lock for the lifetime of the process.

    Usage:
        lock = SingleInstanceLock()
        lock.acquire()   # raises SingleInstanceError if already running
        try:
            ...
        finally:
            lock.release()
    """

    def __init__(self, name: str = _MUTEX_NAME) -> None:
        self._name = name
        self._handle: int | None = None

    def acquire(self) -> None:
        """
        Acquire the single-instance lock.

        Raises:
            SingleInstanceError: If another JARVIS instance already
                holds the lock.
        """

        kernel32 = ctypes.windll.kernel32

        # CreateMutexW returns a handle even if the mutex already
        # existed; GetLastError() tells us whether we created it or
        # merely opened an existing one.
        handle = kernel32.CreateMutexW(None, False, self._name)

        last_error = kernel32.GetLastError()

        if not handle:
            raise SingleInstanceError(
                "Failed to create single-instance lock."
            )

        if last_error == ERROR_ALREADY_EXISTS:
            kernel32.CloseHandle(handle)

            logger.warning(
                "Another JARVIS instance is already running. "
                "Refusing to start a second instance."
            )

            raise SingleInstanceError(
                "JARVIS is already running. Close the other instance "
                "before starting a new one."
            )

        self._handle = handle

        logger.info("Single-instance lock acquired.")

    def release(self) -> None:
        """Release the lock, if held."""

        if self._handle is not None:
            ctypes.windll.kernel32.CloseHandle(self._handle)
            self._handle = None

            logger.info("Single-instance lock released.")

    def __enter__(self) -> "SingleInstanceLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()