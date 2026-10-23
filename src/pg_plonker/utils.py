"""Utility module with helper functions.

Functions:
- get_window_size_from_screen_resolution: Size a window relative to the desktop
  resolution.
- count_decimal_places: Count the decimal digits in a number's shortest string
  form.
"""

from decimal import Decimal

import pygame as pg

from pg_plonker.constants import WINDOW_SIZE_SCREEN_FRACTION


def get_window_size_from_screen_resolution(
    monitor_index: int = 0,
    min_width: int = 400,
    min_height: int = 300,
) -> tuple[int, int]:
    """Compute a windowed (non-fullscreen) size as a fraction of the primary
    desktop resolution.

    1. Initialise the pygame display module if not already active.
    2. Read the desktop resolution via get_desktop_sizes().
    3. Apply WINDOW_SIZE_SCREEN_FRACTION and clamp to the minimum dimensions.

    Args:
        monitor_index (int): Index of the monitor to use from
            get_desktop_sizes().
        min_width (int): Minimum window width in pixels.
        min_height (int): Minimum window height in pixels.

    Returns:
        window_size (tuple[int, int]): The window width and height in pixels.
    """

    if not pg.display.get_init():
        pg.display.init()

    desktop_sizes = pg.display.get_desktop_sizes()
    desktop_size = desktop_sizes[monitor_index]
    desktop_width, desktop_height = desktop_size

    scaled_width = int(desktop_width * WINDOW_SIZE_SCREEN_FRACTION)
    scaled_height = int(desktop_height * WINDOW_SIZE_SCREEN_FRACTION)

    width = max(min_width, scaled_width)
    height = max(min_height, scaled_height)
    window_size = (width, height)

    return window_size


def count_decimal_places(value: int | float) -> int:
    """Count the number of decimal digits in a number's shortest string form.

    Counting is done via Decimal(str(value)) rather than inspecting the raw
    float directly, since binary floating-point numbers do not store decimal
    values exactly (e.g. 0.05 is not represented exactly as 0.05 in memory).
    Going through str() first yields Python's shortest round-trip
    representation, i.e. the digits a human would have actually typed.

    Args:
        value (int | float): The number to inspect.

    Returns:
        decimal_places (int): The number of digits after the decimal point.
    """

    value_text = str(value)
    decimal_value = Decimal(value_text)
    exponent = decimal_value.as_tuple().exponent
    decimal_places = max(-exponent, 0) if isinstance(exponent, int) else 0

    return decimal_places
