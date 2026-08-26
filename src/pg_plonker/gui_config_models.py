"""Module for GUI configuration for the pg_plonker package."""

from dataclasses import dataclass

type RGBColor = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """Configuration container for visual and layout properties of a Button.

    Defines all default styling, sizing, and typography parameters used by
    Button instances when no explicit overrides are provided. This includes
    dimensions, border styling, text rendering settings, and color definitions
    for both active and inactive states.
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
class SliderConfig:
    """Configuration container for visual and layout properties of a Slider.

    Defines all default styling, sizing, and typography parameters used by
    Slider instances when no explicit overrides are provided. This includes
    track and handle dimensions, precision settings for the displayed value, and
    color definitions for the track, handle, border, and value readout.
    """

    # Text and font settings.
    font_name: str = "arial"
    font_size: int = 28

    # Size and distance settings.
    width: int = 540
    height: int = 12
    handle_radius: int = 16
    border_width: int = 3
    margin_vertical: int = 24

    # Number of decimal places added on top of the precision already implied
    # by `start`/`stop`, to keep displayed and dragged values readable while
    # avoiding floating-point noise.
    extra_decimal_places: int = 2

    # Color settings.
    color_track: RGBColor = (150, 150, 150)
    color_track_filled: RGBColor = (200, 150, 150)
    color_handle: RGBColor = (230, 230, 230)
    color_border: RGBColor = (0, 0, 0)
    color_text: RGBColor = (0, 0, 0)


@dataclass(frozen=True)
class DropdownConfig:
    """Configuration container for visual and layout properties of a Dropdown.

    Defines all default styling, sizing, and typography parameters used by
    Dropdown instances when no explicit overrides are provided. This includes
    the closed header's dimensions, the open option list's row height, border
    styling, text rendering settings, and color definitions for the header
    (open/closed), each option row (default/hovered), and the arrow indicator.
    """

    # Text and font settings.
    font_name: str = "arial"
    font_size: int = 32

    # Size and distance settings.
    width: int = 540
    height: int = 72
    option_height: int = 60
    border_width: int = 5
    border_width_inner: int = 3
    text_shadow_offset: int = 3
    arrow_size: int = 14

    # Color settings.
    color_background_active: RGBColor = (200, 150, 150)
    color_background_inactive: RGBColor = (150, 150, 150)
    color_background_option: RGBColor = (170, 170, 170)
    color_background_option_hover: RGBColor = (200, 150, 150)
    color_text: RGBColor = (255, 255, 255)
    color_border: RGBColor = (0, 0, 0)
    color_border_inner_light: RGBColor = (198, 198, 198)
    color_border_inner_dark: RGBColor = (85, 85, 85)
    color_text_shadow: RGBColor = (0, 0, 0)
    color_arrow: RGBColor = (255, 255, 255)


@dataclass(frozen=True)
class GUIPanelConfig:
    """Configuration container for GUI panel layout and styling.

    Defines the default geometry, spacing, alignment, and visual appearance of a
    GUIPanel instance. Controls how the panel is positioned within the main
    surface and how child UI elements are spaced and aligned inside it.
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
