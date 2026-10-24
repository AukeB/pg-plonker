"""Tests for the styles models module."""

import dataclasses

import pytest

from pg_plonker.styles.models import (
    ButtonStyle,
    DropdownStyle,
    PanelStyle,
    RGBColor,
    SliderStyle,
    Style,
)

_PLACEHOLDERS: dict[object, object] = {
    str: "placeholder",
    int: 1,
    float: 0.5,
    bool: False,
    RGBColor: (0, 0, 0),
}

_ELEMENT_STYLES = [ButtonStyle, SliderStyle, DropdownStyle, PanelStyle]


def _placeholder_for(annotation: object) -> object:
    """Return a placeholder value for a field's annotation."""

    if dataclasses.is_dataclass(annotation):
        value = _build(annotation)
    else:
        value = _PLACEHOLDERS[annotation]

    return value


def _build(cls: type) -> object:
    """Build an instance of a style dataclass with a placeholder for every field."""

    values = {
        field.name: _placeholder_for(field.type) for field in dataclasses.fields(cls)
    }
    instance = cls(**values)

    return instance


# Testing the "Style" class.


def test_style_requires_every_element_group_and_switch() -> None:
    with pytest.raises(TypeError):
        Style()


def test_style_groups_the_four_elements_and_the_switches() -> None:
    field_names = {field.name for field in dataclasses.fields(Style)}

    assert field_names == {
        "button",
        "slider",
        "dropdown",
        "panel",
        "hover",
        "hover_lighten",
        "press_bevel",
        "rounded",
        "corner_radius",
    }


def test_style_is_frozen() -> None:
    style = _build(Style)

    with pytest.raises(dataclasses.FrozenInstanceError):
        style.hover = True  # type: ignore[misc]


# Testing the element style classes.


@pytest.mark.parametrize("element_style", _ELEMENT_STYLES)
def test_element_style_requires_every_field(element_style: type) -> None:
    with pytest.raises(TypeError):
        element_style()


@pytest.mark.parametrize("element_style", _ELEMENT_STYLES)
def test_element_style_is_frozen(element_style: type) -> None:
    instance = _build(element_style)
    first_field = dataclasses.fields(element_style)[0].name

    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, first_field, None)


def test_panel_style_holds_visual_values_only() -> None:
    field_names = {field.name for field in dataclasses.fields(PanelStyle)}

    assert field_names == {"border_width", "color_background", "color_border"}
