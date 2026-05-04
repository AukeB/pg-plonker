"""Module for the stateful Button control."""

import pygame as pg
from pygame import Rect, Surface
from pygame.font import Font

from src.pg_plonker import draw
from src.pg_plonker.gui_config_models import ButtonConfig, UIConfig

_default = UIConfig()


class Button:
    """A stateful toggle button that delegates rendering to draw.button."""

    def __init__(
        self,
        surface: Surface,
        rect: Rect,
        text: str,
        font: Font | None = None,
        state: bool = False,
        config: ButtonConfig = _default.button,
    ) -> None:
        """
        Initialize the button with its surface, position, label, and initial state.

        Args:
            surface (Surface): The pygame surface to draw onto.
            rect (Rect): The position and dimensions of the button.
            text (str): Label rendered inside the button.
            font (Font): Pygame font used to render the label.
            config (ButtonConfig): Visual configuration for the button.
            state (bool): Initial toggle state, defaults to False (inactive).
        """
        # Display.
        self.surface = surface
        self.rect = rect
        self.text = text
        self.font = font or pg.font.SysFont(config.font_type, config.font_size)
        self.config = config

        # State.
        self.state = state

        # Other
        self._pressed = False

    def draw(self) -> None:
        """Draw the button reflecting the current toggle state."""
        background_color = (
            self.config.color_background_active
            if self.state
            else self.config.color_background_inactive
        )

        draw.button(
            surface=self.surface,
            rect=self.rect,
            text=self.text,
            font=self.font,
            config=self.config,
            background_color=background_color,
        )

    def handle_event(self, event: pg.event.Event) -> bool:
        """
        Toggle state if the event is a left click inside the button rect.

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
