"""Tests for the terminal style module."""

from pg_plonker.styles.terminal import TERMINAL
from pg_plonker.styles.models import Style

# Testing the "TERMINAL" style.


def test_terminal_is_a_style() -> None:
    assert isinstance(TERMINAL, Style)


def test_terminal_uses_monospace_fonts() -> None:
    assert "monospace" in TERMINAL.button.font_name
    assert TERMINAL.button.font_name == TERMINAL.slider.font_name == TERMINAL.dropdown.font_name


def test_terminal_is_green_on_black() -> None:
    red, green, blue = TERMINAL.button.color_text
    background_red, background_green, background_blue = TERMINAL.panel.color_background

    assert green > red and green > blue
    assert background_red + background_green + background_blue < 30


def test_terminal_has_no_hover_or_rounded_corners_and_has_a_press_bevel() -> None:
    assert TERMINAL.hover is False
    assert TERMINAL.press_bevel is True
    assert TERMINAL.rounded is False


def test_terminal_on_button_stands_out_from_off() -> None:
    on = TERMINAL.button.color_background_active
    off = TERMINAL.button.color_background_inactive

    assert sum(on) - sum(off) >= 120


def test_terminal_press_bevel_light_and_dark_differ() -> None:
    assert TERMINAL.button.color_border_inner_light != TERMINAL.button.color_border_inner_dark


def test_terminal_button_dark_edge_stands_out_from_the_panel() -> None:
    dark_edge = TERMINAL.button.color_border_inner_dark
    panel = TERMINAL.panel.color_background

    assert sum(dark_edge) - sum(panel) >= 90
