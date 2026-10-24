"""Module for the style registry and the active style.

Functions:
- set_style: Make the named style the active style for every control and draw
  call.
- get_style: Return the active style.
"""

from pg_plonker.constants import DEFAULT_STYLE
from pg_plonker.errors import StyleNotFoundError
from pg_plonker.styles.embossed import EMBOSSED
from pg_plonker.styles.flat import FLAT
from pg_plonker.styles.models import Style
from pg_plonker.styles.soft import SOFT
from pg_plonker.styles.terminal import TERMINAL

_STYLES: dict[str, Style] = {
    "embossed": EMBOSSED,
    "flat": FLAT,
    "soft": SOFT,
    "terminal": TERMINAL,
}

_active_style: Style = _STYLES[DEFAULT_STYLE]


def set_style(name: str) -> None:
    """Make the named style the active style.

    The change applies to every control and draw call, including controls that
    were created before this call.

    Args:
        name (str): Name of a registered style, such as "embossed".

    Raises:
        StyleNotFoundError: If no style is registered under the given name.
    """

    global _active_style

    if name not in _STYLES:
        raise StyleNotFoundError(f"No style named {name!r} is registered.")

    _active_style = _STYLES[name]


def get_style() -> Style:
    """Return the active style.

    Returns:
        style (Style): The style that controls and draw calls currently use.
    """

    return _active_style
