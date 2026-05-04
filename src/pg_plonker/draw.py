"""Module for stateless pygame drawing functions for UI elements."""

import pygame as pg
from pygame import Rect, Surface
from pygame.font import Font

from src.pg_plonker.gui_config_models import ButtonConfig, RGBColor, UIConfig

_default = UIConfig()


def button(
    surface: Surface,
    rect: Rect,
    text: str,
    font: Font,
    config: ButtonConfig = _default.button,
    background_color: RGBColor | None = None,
    border_color: RGBColor | None = None,
    text_color: RGBColor | None = None,
    text_shadow_color: RGBColor | None = None,
    border_width: int | None = None,
    border_width_inner: int | None = None,
    text_shadow_offset: int | None = None,
) -> None:
    """
    Draw a single button onto the given surface.

    Args:
        surface (Surface): The pygame surface to draw onto.
        rect (Rect): The position and dimensions of the button.
        text (str): Label to render centered inside the button.
        font (Font): Pygame font used to render the label.
        config (ButtonConfig): Source of default visual parameters.
        background_color (RGBColor | None): Fill color, overrides config if provided.
        border_color (RGBColor | None): Border color, overrides config if provided.
        text_color (RGBColor | None): Text color, overrides config if provided.
        text_shadow_color (RGBColor | None): Shadow color, overrides config if provided.
        border_width (int | None): Border thickness in pixels, overrides config if provided.
        text_shadow_offset (int | None): Shadow offset in pixels, overrides config if provided.
    """
    background_color = background_color or config.color_background_inactive
    border_color = border_color or config.color_border
    text_color = text_color or config.color_text
    text_shadow_color = text_shadow_color or config.color_text_shadow
    border_width = border_width or config.border_width
    border_width_inner = border_width_inner or config.border_width_inner
    shadow_offset = text_shadow_offset or config.shadow_offset
    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)

    pg.draw.rect(surface, background_color, rect)
    pg.draw.rect(surface, border_color, rect, border_width)

    pg.draw.line(
        surface,
        config.color_border_inner_light,
        inner_rect.topleft,
        inner_rect.topright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        config.color_border_inner_light,
        inner_rect.topleft,
        inner_rect.bottomleft,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        config.color_border_inner_dark,
        inner_rect.bottomleft,
        inner_rect.bottomright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        config.color_border_inner_dark,
        inner_rect.topright,
        inner_rect.bottomright,
        border_width_inner,
    )

    shadow_surface = font.render(text, True, text_shadow_color)
    shadow_rect = shadow_surface.get_rect(
        center=(
            rect.centerx + shadow_offset,
            rect.centery + shadow_offset,
        )
    )
    surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
