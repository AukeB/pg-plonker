"""Checks that apply to every registered style."""

import dataclasses

import pytest

from pg_plonker.styles import get_style, set_style
from pg_plonker.styles.registry import _STYLES
from pg_plonker.styles.models import (
    ButtonStyle,
    DropdownStyle,
    PanelStyle,
    SliderStyle,
    Style,
)

_ELEMENT_GROUPS = [
    ("button", ButtonStyle),
    ("slider", SliderStyle),
    ("dropdown", DropdownStyle),
    ("panel", PanelStyle),
]
_ALL_STYLES = list(_STYLES.items())


def _is_rgb(value: object) -> bool:
    """True when the value is an (r, g, b) tuple of ints from 0 to 255."""

    is_tuple = isinstance(value, tuple) and len(value) == 3
    is_channels = is_tuple and all(
        isinstance(channel, int) and not isinstance(channel, bool) and 0 <= channel <= 255
        for channel in value
    )

    return is_channels


def _check_value_for_annotation(value: object, annotation: object) -> bool:
    """True when a value matches the annotation of a style field."""

    if annotation is bool:
        matches = isinstance(value, bool)
    elif annotation is int:
        matches = isinstance(value, int) and not isinstance(value, bool)
    elif annotation is float:
        matches = isinstance(value, (int, float)) and not isinstance(value, bool)
    elif annotation is str:
        matches = isinstance(value, str) and value != ""
    else:
        matches = _is_rgb(value)

    return matches


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_every_field_is_set_to_a_value_of_the_right_type(name: str, style: Style) -> None:
    for group, element_style in _ELEMENT_GROUPS:
        element = getattr(style, group)
        assert isinstance(element, element_style), (name, group)
        for field in dataclasses.fields(element_style):
            value = getattr(element, field.name)

            assert _check_value_for_annotation(value, field.type), (name, group, field.name, value)


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_every_switch_is_set_to_a_value_of_the_right_type(name: str, style: Style) -> None:
    switches = ("hover", "hover_lighten", "press_bevel", "rounded", "corner_radius")
    for switch in switches:
        field = next(f for f in dataclasses.fields(Style) if f.name == switch)
        value = getattr(style, switch)

        assert _check_value_for_annotation(value, field.type), (name, switch, value)


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_hover_lighten_is_a_fraction_and_radius_is_not_negative(name: str, style: Style) -> None:
    assert 0 <= style.hover_lighten <= 1
    assert style.corner_radius >= 0


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_a_press_bevel_has_visible_light_and_dark_edges(name: str, style: Style) -> None:
    if style.press_bevel:
        assert style.button.border_width_inner > 0, name
        assert style.button.color_border_inner_light != style.button.color_border_inner_dark, name


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_a_rounded_style_has_a_positive_corner_radius(name: str, style: Style) -> None:
    if style.rounded:
        assert style.corner_radius > 0, name


@pytest.mark.parametrize(("name", "style"), _ALL_STYLES)
def test_each_style_can_be_selected_by_its_name(name: str, style: Style) -> None:
    set_style(name)
    try:
        assert get_style() is style
    finally:
        set_style("embossed")
