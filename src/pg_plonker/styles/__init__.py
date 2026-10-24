"""Style definitions for pg-plonker.

Modules:
- models: The style dataclasses every style fills in.
- embossed: The embossed style, the default.
- registry: The style registry, set_style() and get_style().

Functions:
- set_style: Make the named style the active style.
- get_style: Return the active style.
"""

from pg_plonker.styles.registry import get_style, set_style

__all__ = [
    "get_style",
    "set_style",
]
