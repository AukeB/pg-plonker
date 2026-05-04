"""Module for GUI configuration for the pg_plonker package."""

from dataclasses import dataclass, field

type RGBColor = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """ """

    # Related to sizes.
    width: int = 540
    height: int = 108
    border_width: int = 5
    border_width_inner: int = 3
    shadow_offset: int = 3

    # Related to the font.
    font_type: str = "arial"
    font_size: int = 50

    # Related to colors.
    color_background_active: RGBColor = (200, 150, 150)
    color_background_inactive: RGBColor = (150, 150, 150)
    color_text: RGBColor = (255, 255, 255)
    color_border: RGBColor = (0, 0, 0)
    color_border_inner_light: RGBColor = (198, 198, 198)
    color_border_inner_dark: RGBColor = (85, 85, 85)
    color_text_shadow: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class PanelConfig:
    """ """

    width: int = 220
    border_width: int = 2
    color_background: RGBColor = (255, 255, 255)
    color_border: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class UIConfig:
    """Top-level configuration for the pygame UI panel and its controls."""

    panel: PanelConfig = field(default_factory=PanelConfig)
    button: ButtonConfig = field(default_factory=ButtonConfig)
