"""Utility module with helper functions."""

import pygame as pg

from pg_plonker.constants import WINDOW_SIZE_SCREEN_FRACTION

_font_cache: dict[tuple[str, int], pg.font.Font] = {}


def get_font(font_name: str, font_size: int) -> pg.font.Font:
    """
    Retrieve a font from cache, creating and caching it if not yet loaded.

    pg.font.SysFont is expensive to call and should never be invoked
    every frame. This function ensures each unique (font_name, font_size)
    combination is created only once and reused for all subsequent calls.

    Args:
        font_name (str): The system font name to load.
        font_size (int): The font size in points.

    Returns:
        font (pg.font.Font): The cached font object.
    """
    key = (font_name, font_size)
    if key not in _font_cache:
        _font_cache[key] = pg.font.SysFont(name=font_name, size=font_size)
    result = _font_cache[key]

    return result


def get_window_size_from_screen_resolution(
    monitor_index: int = 0,
    min_width: int = 400,
    min_height: int = 300,
) -> tuple[int, int]:
    """
    Compute a windowed (non-fullscreen) size as a fraction of the primary desktop resolution.

    1. Initialise the pygame display module if not already active.
    2. Attempt to read the desktop resolution via get_desktop_sizes() (pygame >= 2.0).
    3. Fall back to display.Info() for older pygame versions.
    4. Apply WINDOW_SIZE_SCREEN_FRACTION and clamp to the minimum dimensions.

    Args:
        monitor_index (int): Index of the monitor to use from get_desktop_sizes().
        min_width (int): Minimum window width in pixels.
        min_height (int): Minimum window height in pixels.

    Returns:
        tuple[int, int]: The window width and height in pixels.
    """
    # Init
    if not pg.display.get_init():
        pg.display.init()

    # Resolve desktop resolution
    if pg.version.vernum >= (2, 0, 0):
        desktop_width, desktop_height = pg.display.get_desktop_sizes()[monitor_index]
    else:
        info = pg.display.Info()
        desktop_width = info.current_w if info.current_w > 0 else 1920
        desktop_height = info.current_h if info.current_h > 0 else 1080

    # Scale
    width = max(min_width, int(desktop_width * WINDOW_SIZE_SCREEN_FRACTION))
    height = max(min_height, int(desktop_height * WINDOW_SIZE_SCREEN_FRACTION))

    return width, height
