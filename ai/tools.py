"""
Will define the Tool interface (name, description, parameter schema,
execute()) and a registry the LLM's function-calling can select from.

This is the abstraction that replaces "hundreds of if/elif statements"
with a structured, extensible tool system.

Not implemented yet — this arrives in Phase 3 (V1), after basic
conversation (Phase 1-2) is stable.
"""

from __future__ import annotations

# Implementation begins in Phase 3.