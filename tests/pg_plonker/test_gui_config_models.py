"""Tests for the gui_config_models module."""

import dataclasses

import pytest

from pg_plonker.gui_config_models import (
    ButtonConfig,
    DropdownConfig,
    GUIPanelConfig,
    SliderConfig,
)

# Testing the default values of the config dataclasses.


@pytest.mark.parametrize("config_class", [ButtonConfig, SliderConfig, DropdownConfig, GUIPanelConfig])
def test_config_defaults_are_frozen(config_class: type) -> None:
    config = config_class()

    assert dataclasses.is_dataclass(config)

    with pytest.raises(dataclasses.FrozenInstanceError):
        config.width = 1  # type: ignore[misc]


def test_button_config_default_size() -> None:
    assert ButtonConfig().width == 540
    assert ButtonConfig().height == 108
