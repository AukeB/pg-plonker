"""Tests for the constants module."""

from pg_plonker.constants import DEFAULT_STYLE, WINDOW_SIZE_SCREEN_FRACTION


# Testing the "WINDOW_SIZE_SCREEN_FRACTION" constant.


def test_window_size_fraction_leaves_room_on_the_desktop() -> None:
    assert 0 < WINDOW_SIZE_SCREEN_FRACTION < 1


# Testing the "DEFAULT_STYLE" constant.


def test_default_style_is_embossed() -> None:
    assert DEFAULT_STYLE == "embossed"
