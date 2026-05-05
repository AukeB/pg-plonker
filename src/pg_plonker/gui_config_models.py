"""Module for GUI configuration for the pg_plonker package."""

from dataclasses import dataclass, field

import pygame as pg
from pygame.font import Font

type RGBColor = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """ """

    # Text and font settings.
    text: str = "Button"
    font_name: str = "arial"
    font_size: int = 50

    # Size and distance settings.
    width: int = 540
    height: int = 108
    border_width: int = 5
    border_width_inner: int = 3
    text_shadow_offset: int = 3

    # Color settings.
    color_background_active: RGBColor = (200, 150, 150)
    color_background_inactive: RGBColor = (150, 150, 150)
    color_text: RGBColor = (255, 255, 255)
    color_border: RGBColor = (0, 0, 0)
    color_border_inner_light: RGBColor = (198, 198, 198)
    color_border_inner_dark: RGBColor = (85, 85, 85)
    color_text_shadow: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class GUIPanelConfig:
    """ """

    # Size and distance settings.
    width: int = 620
    border_width: int = 2
    margin_gui_panel: int = 20
    margin_button: int = 12

    # Position
    align_right: bool = True

    # Color settings.
    color_background: RGBColor = (230, 230, 230)
    color_border: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class PGPlonkerConfig:
    """Top-level configuration for the pg_plonker package."""

    gui_panel: GUIPanelConfig = field(default_factory=GUIPanelConfig)
    button: ButtonConfig = field(default_factory=ButtonConfig)
