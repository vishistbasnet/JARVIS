"""
Centralized logging configuration for JARVIS.

Every module gets its logger via `get_logger(__name__)` instead of configuring
logging itself. This keeps log format, log level, and log destinations
consistent across the whole application, and gives us one place to change
behavior (e.g. switching to JSON logs later) without touching every file.

IMPORTANT: Never log secrets (API keys, passwords, tokens). Modules are
responsible for not passing secrets into log calls; this module does not
attempt to redact arbitrary strings, since that's unreliable. See
config.py for how secrets are kept out of anything printable/loggable.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Directory where log files are written. Created on first use.
LOG_DIR = Path(__file__).resolve().parent.parent / "data" / "logs"
LOG_FILE = LOG_DIR / "jarvis.log"

# Keep log files from growing forever: 5 MB per file, keep 3 old copies.
MAX_LOG_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def _configure_root_logger(level: int = logging.INFO) -> None:
    """
    Configure the root logger exactly once per process.

    Adds two handlers:
      - a console handler (so you see logs while developing)
      - a rotating file handler (so you have a persistent record to debug
        issues after the fact, e.g. "why did the microphone fail last night")
    """
    global _configured
    if _configured:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # file keeps more detail than console

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Third-party libraries (e.g. urllib3, whisper) can be extremely noisy at
    # DEBUG/INFO. Quiet them down by default; raise if you need to debug them.
    for noisy_logger in ("urllib3", "httpx", "httpcore"):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger for a module.

    Usage:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Something happened")

    Args:
        name: Usually `__name__` of the calling module, so log lines show
            exactly which file/module produced them.
        level: Console log level for this specific logger. Defaults to INFO.
            The file handler always captures DEBUG and above regardless.
    """
    _configure_root_logger()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger