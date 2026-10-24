"""Tests for the soft style module."""

from pg_plonker.styles.soft import SOFT
from pg_plonker.styles.models import Style

# Testing the "SOFT" style.


def test_soft_is_a_style() -> None:
    assert isinstance(SOFT, Style)


def test_soft_has_subtle_shadows() -> None:
    assert 0 < SOFT.button.text_shadow_offset <= 3
    assert 0 < SOFT.dropdown.text_shadow_offset <= 3


def test_soft_uses_light_backgrounds() -> None:
    assert min(SOFT.panel.color_background) > 200
    assert min(SOFT.button.color_background_inactive) > 200


def test_soft_has_no_rounded_corners() -> None:
    assert SOFT.rounded is False


def test_soft_has_a_press_bevel_with_light_and_dark_edges() -> None:
    assert SOFT.press_bevel is True
    assert SOFT.button.border_width_inner > 0
    assert SOFT.button.color_border_inner_light != SOFT.button.color_border_inner_dark
