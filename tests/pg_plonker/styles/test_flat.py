"""Tests for the flat style module."""

from pg_plonker.styles.flat import FLAT
from pg_plonker.styles.models import Style

# Testing the "FLAT" style.


def test_flat_is_a_style() -> None:
    assert isinstance(FLAT, Style)


def test_flat_has_no_hover_press_bevel_or_rounded_corners() -> None:
    assert FLAT.hover is False
    assert FLAT.press_bevel is False
    assert FLAT.rounded is False


def test_flat_has_no_borders_or_bevels() -> None:
    assert FLAT.button.border_width == 0
    assert FLAT.button.border_width_inner == 0
    assert FLAT.slider.box_border_width == 0
    assert FLAT.slider.border_width == 0
    assert FLAT.dropdown.border_width == 0
    assert FLAT.panel.border_width == 0
