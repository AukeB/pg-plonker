"""Tests for the chalk style module."""

import pytest

from pg_plonker.styles.chalk import CHALK
from pg_plonker.styles.models import Style
from pg_plonker.utils import lighten_color

# Testing the "CHALK" style.


def _relative_luminance(color: tuple[int, int, int]) -> float:
    """Return the WCAG relative luminance of an RGB colour."""

    linear = []
    for channel in color:
        scaled = channel / 255
        if scaled <= 0.03928:
            linear.append(scaled / 12.92)
        else:
            linear.append(((scaled + 0.055) / 1.055) ** 2.4)

    red, green, blue = linear
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue

    return luminance


def _contrast_ratio(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    """Return the WCAG contrast ratio between two RGB colours."""

    lighter = max(_relative_luminance(first), _relative_luminance(second))
    darker = min(_relative_luminance(first), _relative_luminance(second))

    return (lighter + 0.05) / (darker + 0.05)


def test_chalk_is_a_style() -> None:
    assert isinstance(CHALK, Style)


def test_chalk_is_rounded_without_press_bevel() -> None:
    assert CHALK.rounded is True
    assert CHALK.corner_radius > 0
    assert CHALK.press_bevel is False


def test_chalk_on_state_is_yellow() -> None:
    red, green, blue = CHALK.button.color_background_active

    assert red > 200
    assert green > 150
    assert blue < 120


@pytest.mark.parametrize(
    ("text", "background"),
    [
        (CHALK.button.color_text, CHALK.button.color_background_inactive),
        (CHALK.button.color_text, CHALK.button.color_background_active),
        (CHALK.dropdown.color_text, CHALK.dropdown.color_background_inactive),
        (CHALK.dropdown.color_text, CHALK.dropdown.color_background_active),
        (CHALK.dropdown.color_text, CHALK.dropdown.color_background_option),
        (CHALK.dropdown.color_text, CHALK.dropdown.color_background_option_hover),
        (CHALK.slider.color_text, CHALK.slider.color_box_background),
    ],
)
def test_chalk_text_is_readable_on_its_background(
    text: tuple[int, int, int], background: tuple[int, int, int]
) -> None:
    assert _contrast_ratio(text, background) >= 4.5


@pytest.mark.parametrize(
    ("text", "background"),
    [
        (CHALK.button.color_text, CHALK.button.color_background_inactive),
        (CHALK.button.color_text, CHALK.button.color_background_active),
        (CHALK.dropdown.color_text, CHALK.dropdown.color_background_inactive),
    ],
)
def test_chalk_text_stays_readable_when_hovered(
    text: tuple[int, int, int], background: tuple[int, int, int]
) -> None:
    hovered = lighten_color(background, CHALK.hover_lighten)

    assert _contrast_ratio(text, hovered) >= 4.5
