"""Shared pytest fixtures. PyGame runs headless so the tests can open windows without a monitor."""

import os
from collections.abc import Iterator

import pygame as pg
import pytest

from pg_plonker import utils


@pytest.fixture(scope="session", autouse=True, name="headless_pygame")
def fixture_headless_pygame() -> None:
    """Use the dummy SDL drivers, so windows and audio work without hardware."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(name="screen")
def fixture_screen() -> Iterator[pg.Surface]:
    """Provide a black 800 x 600 window surface, and shut pygame down afterwards.

    Yields:
        screen (pg.Surface): The display surface.
    """

    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen.fill((0, 0, 0))

    yield screen

    # Cached fonts belong to the pygame session that created them, so drop them before quitting.
    utils._font_cache.clear()
    pg.quit()
