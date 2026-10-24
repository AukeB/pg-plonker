"""Tests for the embossed style module."""

from pg_plonker.styles.embossed import EMBOSSED
from pg_plonker.styles.models import Style

# Testing the "EMBOSSED" style.


def test_embossed_is_a_style() -> None:
    assert isinstance(EMBOSSED, Style)


def test_embossed_has_raised_bevels_with_light_above_dark() -> None:
    assert EMBOSSED.button.color_border_inner_light != EMBOSSED.button.color_border_inner_dark
    assert EMBOSSED.press_bevel is True


def test_embossed_is_not_rounded() -> None:
    assert EMBOSSED.rounded is False


def test_embossed_button_on_and_off_backgrounds_are_clearly_different() -> None:
    on = EMBOSSED.button.color_background_active
    off = EMBOSSED.button.color_background_inactive

    assert all(abs(a - b) >= 40 for a, b in zip(on, off, strict=True))


def test_embossed_dropdown_header_on_and_off_backgrounds_are_clearly_different() -> None:
    open_color = EMBOSSED.dropdown.color_background_active
    closed_color = EMBOSSED.dropdown.color_background_inactive

    assert all(abs(a - b) >= 40 for a, b in zip(open_color, closed_color, strict=True))


def test_embossed_slider_label_is_larger_than_the_value() -> None:
    assert EMBOSSED.slider.label_font_size > EMBOSSED.slider.font_size
