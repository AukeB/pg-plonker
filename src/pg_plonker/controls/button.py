"""Module for the stateful Button control."""

import pygame as pg
from pygame import Rect, Surface

from src.pg_plonker import draw
from src.pg_plonker.gui_config_models import ButtonConfig, RGBColor

_config_button = ButtonConfig()


class Button:
    """A stateful toggle button that delegates rendering to draw.button."""

    def __init__(
        self,
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
        color_background_active: RGBColor | None = None,
        color_background_inactive: RGBColor | None = None,
        color_text: RGBColor | None = None,
        color_border: RGBColor | None = None,
        color_border_inner_light: RGBColor | None = None,
        color_border_inner_dark: RGBColor | None = None,
        color_text_shadow: RGBColor | None = None,
        state: bool = False,
    ) -> None:
        """
        Initialize the button with its surface, position, and visual parameters.

        All visual parameters are optional and fall back to the module-level
        PGPlonkerConfig when not provided. They are stored as-is and forwarded
        to draw.button each frame, where the fallback logic is applied.

        Args:
            surface (Surface): The pygame surface to draw onto.
            rect (Rect): The position and dimensions of the button.
            text (str | None): Label rendered inside the button.
            font_name (str | None): System font name.
            font_size (int | None): Font size in points.
            border_width (int | None): Outer border thickness in pixels.
            border_width_inner (int | None): Inner border thickness in pixels.
            text_shadow_offset (int | None): Shadow offset in pixels.
            color_background_active (RGBColor | None): Fill color when active.
            color_background_inactive (RGBColor | None): Fill color when inactive.
            color_text (RGBColor | None): Text color.
            color_border (RGBColor | None): Outer border color.
            color_border_inner_light (RGBColor | None): Light inner border color.
            color_border_inner_dark (RGBColor | None): Dark inner border color.
            color_text_shadow (RGBColor | None): Text shadow color.
            state (bool): Initial toggle state, defaults to False.
        """
        # Display.
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width or _config_button.width
        self.height = height or _config_button.height
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.border_width = border_width
        self.border_width_inner = border_width_inner
        self.text_shadow_offset = text_shadow_offset
        self.color_background_active = (
            color_background_active or _config_button.color_background_active
        )
        self.color_background_inactive = (
            color_background_inactive or _config_button.color_background_inactive
        )
        self.color_text = color_text
        self.color_border = color_border
        self.color_border_inner_light = color_border_inner_light
        self.color_border_inner_dark = color_border_inner_dark
        self.color_text_shadow = color_text_shadow

        # Definitions depending on function/config input.
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        # State.
        self.state = state
        self._pressed = False

    def draw(self) -> None:
        """Draw the button reflecting the current toggle state."""
        color_background = (
            self.color_background_active
            if self.state
            else self.color_background_inactive
        )

        draw.button(
            surface=self.surface,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            text=self.text,
            font_name=self.font_name,
            font_size=self.font_size,
            border_width=self.border_width,
            border_width_inner=self.border_width_inner,
            text_shadow_offset=self.text_shadow_offset,
            color_background=color_background,
            color_text=self.color_text,
            color_border=self.color_border,
            color_border_inner_light=self.color_border_inner_light,
            color_border_inner_dark=self.color_border_inner_dark,
            color_text_shadow=self.color_text_shadow,
        )

    def handle_event(self, event: pg.event.Event) -> bool:
        """
        Toggle state on mouse release if the button was pressed down on this control.

        Args:
            event (pg.event.Event): The pygame event to handle.

        Returns:
            changed (bool): True if the state changed, False otherwise.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._pressed = True

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self._pressed and self.rect.collidepoint(event.pos):
                self._pressed = False
                self.state = not self.state

                return True

            self._pressed = False

        return False
