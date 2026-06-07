"""Module for stateless pygame drawing functions for UI elements."""

import pygame as pg
from pygame import Surface

from pg_plonker.gui_config_models import ButtonConfig, RGBColor
from pg_plonker.utils import get_font

_config_button = ButtonConfig()


def button(
    surface: Surface,
    x: int,
    y: int,
    width: int | None = None,
    height: int | None = None,
    text: str | None = None,
    font_name: str | None = None,
    font_size: int | None = None,
    border_width: int | None = None,
    border_width_inner: int | None = None,
    text_shadow_offset: int | None = None,
    color_background: RGBColor | None = None,
    color_text: RGBColor | None = None,
    color_border: RGBColor | None = None,
    color_border_inner_light: RGBColor | None = None,
    color_border_inner_dark: RGBColor | None = None,
    color_text_shadow: RGBColor | None = None,
) -> None:
    """Draw a single button onto the given surface.

    All parameters except surface are optional and fall back to the values defined in
    the module- level ButtonConfig when not provided. This allows quick usage with
    minimal arguments while still permitting per-call overrides of any visual property.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position in pixels.
        y (int) Y position in pixels.
        width (int | None): Button width in pixels, overrides config if provided.
        height (int | None): Button height in pixels, overrides config if provided.
        text (str | None): Label to render centered inside the button.
        font_name (str | None): System font name, overrides config if provided.
        font_size (int | None): Font size in points, overrides config if provided.
        border_width (int | None): Outer border thickness in pixels, overrides config if
            provided.
        border_width_inner (int | None): Inner border thickness in pixels, overrides
            config if provided.
        text_shadow_offset (int | None): Shadow offset in pixels, overrides config if
            provided.
        color_background (RGBColor | None): Background fill color, overrides config if
            provided.
        color_text (RGBColor | None): Text color, overrides config if provided.
        color_border (RGBColor | None): Outer border color, overrides config if
            provided.
        color_border_inner_light (RGBColor | None): Light inner border color, overrides
            config if provided.
        color_border_inner_dark (RGBColor | None): Dark inner border color, overrides
            config if provided.
        color_text_shadow (RGBColor | None): Text shadow color, overrides config if
            provided.
    """
    # Get all arguments, either from function input or config.
    width = width or _config_button.width
    height = height or _config_button.height
    text = text or _config_button.text
    font_name = font_name or _config_button.font_name
    font_size = font_size or _config_button.font_size
    border_width = border_width or _config_button.border_width
    border_width_inner = border_width_inner or _config_button.border_width_inner
    text_shadow_offset = text_shadow_offset or _config_button.text_shadow_offset
    color_background = color_background or _config_button.color_background_inactive
    color_text = color_text or _config_button.color_text
    color_border = color_border or _config_button.color_border
    color_border_inner_light = (
        color_border_inner_light or _config_button.color_border_inner_light
    )
    color_border_inner_dark = (
        color_border_inner_dark or _config_button.color_border_inner_dark
    )
    color_text_shadow = color_text_shadow or _config_button.color_text_shadow

    # Definitions depending on function/config input.
    rect = pg.Rect(x, y, width, height)
    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)
    font = get_font(font_name=font_name, font_size=font_size)

    # Drawing operations.
    pg.draw.rect(surface, color_background, rect)
    pg.draw.rect(surface, color_border, rect, border_width)

    pg.draw.line(
        surface,
        color_border_inner_light,
        inner_rect.topleft,
        inner_rect.topright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_light,
        inner_rect.topleft,
        inner_rect.bottomleft,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_dark,
        inner_rect.bottomleft,
        inner_rect.bottomright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_dark,
        inner_rect.topright,
        inner_rect.bottomright,
        border_width_inner,
    )

    shadow_surface = font.render(text, True, color_text_shadow)
    shadow_rect = shadow_surface.get_rect(
        center=(
            rect.centerx + text_shadow_offset,
            rect.centery + text_shadow_offset,
        )
    )
    surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
