"""
JARVIS application entry point.

Starts the real JARVIS voice assistant and keeps it
running until the user stops the program.
"""

from __future__ import annotations

import sys

from core.assistant import Assistant
from utils.logger import get_logger
from utils.single_instance import SingleInstanceError, SingleInstanceLock

logger = get_logger(__name__)


def main() -> int:
    """Start and run JARVIS."""

    logger.info("Starting JARVIS...")

    lock = SingleInstanceLock()

    try:
        lock.acquire()
    except SingleInstanceError:
        print()
        print("=" * 60)
        print("JARVIS IS ALREADY RUNNING")
        print("=" * 60)
        print("Another JARVIS instance is already active on this")
        print("computer. Running two at once can cause voice commands")
        print("(including confirmation replies) to be picked up by the")
        print("wrong instance, so this instance will not start.")
        print("Close the other JARVIS window first.")
        print("=" * 60)
        print()
        return 1

    try:
        assistant = Assistant()

        print()
        print("=" * 60)
        print("JARVIS IS READY")
        print("=" * 60)
        print("Speak a command.")
        print("Press Ctrl+C to stop JARVIS.")
        print("=" * 60)
        print()

        while True:
            assistant.process_once()

    except KeyboardInterrupt:
        logger.info("JARVIS stopped by user.")
        print("\nJARVIS stopped.")
        return 0

    except Exception:
        logger.exception("JARVIS stopped because of an unexpected error.")
        print("\nJARVIS encountered an unexpected error.")
        print("Check the logs for details.")
        return 1

    finally:
        lock.release()


if __name__ == "__main__":
    sys.exit(main())