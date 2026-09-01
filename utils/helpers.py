"""
Small, generic helper functions shared across modules.

Keep this file for genuinely reusable, dependency-light utilities only.
Anything tied to a specific feature (weather formatting, email formatting,
etc.) belongs in that feature's own module, not here.
"""

from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, TypeVar

from utils.logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def timed(func: F) -> F:
    """
    Decorator that logs how long a function took to run, at DEBUG level.

    Useful for spotting latency issues (e.g. "is STT or the LLM call the
    slow part of the pipeline?") without adding manual timing code
    everywhere.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.debug("%s took %.1f ms", func.__qualname__, elapsed_ms)

    return wrapper  # type: ignore[return-value]


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate text for safe/readable logging, appending '...' if cut."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."