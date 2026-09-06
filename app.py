"""
JARVIS application entry point.

Starts the real JARVIS voice assistant and keeps it
running until the user stops the program.
"""

from __future__ import annotations

import sys

from core.assistant import Assistant
from utils.logger import get_logger

logger = get_logger(__name__)


def main() -> int:
    """Start and run JARVIS."""

    logger.info("Starting JARVIS...")

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


if __name__ == "__main__":
    sys.exit(main())