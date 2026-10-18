"""Tests for the constants module."""

from pg_plonker.constants import WINDOW_SIZE_SCREEN_FRACTION


# Testing the "WINDOW_SIZE_SCREEN_FRACTION" constant.


def test_window_size_fraction_leaves_room_on_the_desktop() -> None:
    assert 0 < WINDOW_SIZE_SCREEN_FRACTION < 1
