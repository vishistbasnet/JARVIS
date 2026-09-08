"""
JARVIS error types.

Defines application-level exceptions so the assistant can
distinguish recoverable failures from unexpected programming errors.
"""

from __future__ import annotations


class JarvisError(Exception):
    """Base exception for expected JARVIS failures."""


class TransientError(JarvisError):
    """A temporary failure that may succeed if retried."""


class LLMError(JarvisError):
    """An expected LLM/provider failure."""


class ToolExecutionError(JarvisError):
    """A tool failed while being executed."""


class SpeechError(JarvisError):
    """Speech recognition failed."""


class TTSError(JarvisError):
    """Text-to-speech failed."""