"""Tests for the utils module."""

import math

import pygame as pg
import pytest

from pg_plonker.utils import (
    count_decimal_places,
    get_window_size_from_screen_resolution,
)

# Testing the "get_window_size_from_screen_resolution" function.


def test_window_size_scales_the_desktop_size(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pg.display, "get_desktop_sizes", lambda: [(1920, 1080)])

    window_size = get_window_size_from_screen_resolution()

    assert window_size == (1728, 972)


def test_window_size_clamps_to_minimum(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pg.display, "get_desktop_sizes", lambda: [(100, 100)])

    window_size = get_window_size_from_screen_resolution()

    assert window_size == (400, 300)


def test_window_size_initializes_display_when_needed(monkeypatch: pytest.MonkeyPatch) -> None:
    initialized: list[bool] = []
    monkeypatch.setattr(pg.display, "get_init", lambda: False)

    def record_init() -> None:
        initialized.append(True)

    monkeypatch.setattr(pg.display, "init", record_init)
    monkeypatch.setattr(pg.display, "get_desktop_sizes", lambda: [(1920, 1080)])

    get_window_size_from_screen_resolution()

    assert initialized == [True]


# Testing the "count_decimal_places" function.


@pytest.mark.parametrize(
    ("value", "expected"),
    [(5, 0), (2.5, 1), (0.05, 2), (1e-7, 7), (1e20, 0), (math.inf, 0)],
)
def test_count_decimal_places_counts_shortest_form(value: float, expected: int) -> None:
    assert count_decimal_places(value) == expected
