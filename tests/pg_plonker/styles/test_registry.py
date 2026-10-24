"""Tests for the style registry."""

import dataclasses
from collections.abc import Iterator

import pygame as pg
import pytest

from pg_plonker.controls import Button
from pg_plonker.errors import StyleNotFoundError
from pg_plonker.styles.registry import _STYLES, get_style, set_style
from pg_plonker.styles.embossed import EMBOSSED
from pg_plonker.styles.flat import FLAT
from pg_plonker.styles.soft import SOFT
from pg_plonker.styles.terminal import TERMINAL


@pytest.fixture(name="restore_style", autouse=True)
def fixture_restore_style() -> Iterator[None]:
    """Make the default style active again after each test."""

    yield

    set_style("embossed")


# Testing the "set_style" function.


def test_set_style_rejects_an_unknown_name() -> None:
    with pytest.raises(StyleNotFoundError, match="no-such-style"):
        set_style("no-such-style")


def test_set_style_makes_the_named_style_active(monkeypatch: pytest.MonkeyPatch) -> None:
    other = dataclasses.replace(
        EMBOSSED, button=dataclasses.replace(EMBOSSED.button, width=123)
    )
    monkeypatch.setitem(_STYLES, "other", other)

    set_style("other")

    assert get_style() is other


def test_existing_controls_follow_a_later_set_style(
    screen: pg.Surface, monkeypatch: pytest.MonkeyPatch
) -> None:
    other = dataclasses.replace(
        EMBOSSED, button=dataclasses.replace(EMBOSSED.button, width=123)
    )
    monkeypatch.setitem(_STYLES, "other", other)
    button = Button(surface=screen, x=20, y=20)

    set_style("other")

    assert button.width == 123
    assert button.rect.width == 123


# Testing the "get_style" function.


def test_get_style_starts_as_the_default_style() -> None:
    assert get_style() is EMBOSSED


def test_set_style_can_select_flat() -> None:
    set_style("flat")

    assert get_style() is FLAT


def test_set_style_can_select_terminal_and_soft() -> None:
    set_style("terminal")
    assert get_style() is TERMINAL

    set_style("soft")
    assert get_style() is SOFT
