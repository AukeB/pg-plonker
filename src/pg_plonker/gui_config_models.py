"""Module for GUI configuration for the pg_plonker package."""

from dataclasses import dataclass, field

type RGBColor = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """Configuration container for visual and layout properties of a Button.

    Defines all default styling, sizing, and typography parameters used by Button
    instances when no explicit overrides are provided. This includes dimensions, border
    styling, text rendering settings, and color definitions for both active and inactive
    states.
    """

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
    """Configuration container for GUI panel layout and styling.

    Defines the default geometry, spacing, alignment, and visual appearance of a
    GUIPanel instance. Controls how the panel is positioned within the main surface and
    how child UI elements are spaced and aligned inside it.
    """

    # Size and distance settings.
    width: int = 620
    border_width: int = 2
    margin_gui_panel: int = 40
    margin_button: int = 24

    # Position
    align_right: bool = True

    # Color settings.
    color_background: RGBColor = (230, 230, 230)
    color_border: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class PGPlonkerConfig:
    """Root configuration object for the pg_plonker UI system.

    Aggregates all sub-configurations (such as GUI panel and button settings) into a
    single immutable configuration structure. Intended as the top-level entry point for
    global UI styling and layout defaults.
    """

    gui_panel: GUIPanelConfig = field(default_factory=GUIPanelConfig)
    button: ButtonConfig = field(default_factory=ButtonConfig)
