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
