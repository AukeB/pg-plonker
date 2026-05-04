"""Module for the UIPanel control container."""

import pygame as pg
from pygame import Rect, Surface

from src.pg_plonker.controls.button import Button
from src.pg_plonker.gui_config_models import GUIPanelConfig, PGPlonkerConfig

_default = PGPlonkerConfig()

_BUTTON_GAP: int = 12
_PANEL_PADDING_TOP: int = 20


class GUIPanel:
    """A side panel that owns and lays out stateful controls."""

    def __init__(
        self,
        surface: Surface,
        config: GUIPanelConfig = _default.gui_panel,
        right_side: bool = True,
    ) -> None:
        """
        Initialize the panel and carve out a subsurface for its interior.

        Args:
            surface (Surface): The parent pygame surface to attach the panel to.
            config (PanelConfig): Visual configuration for the panel.
            right_side (bool): If True, panel appears on the right side of the
                window. If False, it appears on the left.
        """
        # Config.
        self.config = config
        self.surface = surface

        # Layout.
        screen_width, screen_height = surface.get_size()
        panel_x = screen_width - config.width if right_side else 0
        self.panel_rect = Rect(panel_x, 0, config.width, screen_height)
        self.subsurface = surface.subsurface(self.panel_rect)

        # Dividing line x position on the parent surface.
        self.divider_x = panel_x if right_side else config.width

        # Controls.
        self._controls: list[Button] = []
        self._next_button_y = _PANEL_PADDING_TOP

    def add(self, button: Button) -> None:
        """
        Register a button with the panel and assign it a stacked position.

        Args:
            button (Button): The button control to add.
        """
        button_x = (self.config.width - button.config.width) // 2
        button.rect = Rect(
            button_x,
            self._next_button_y,
            button.config.width,
            button.config.height,
        )
        # Rebind the button's surface to the panel subsurface so all
        # drawing coordinates are relative to the panel, not the screen.
        button.surface = self.subsurface

        self._next_button_y += button.config.height + _BUTTON_GAP
        self._controls.append(button)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Forward events to all registered controls.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """
        # Translate mouse coordinates from screen space to panel space
        # so collidepoint checks inside buttons work correctly.
        if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION):
            translated = event.copy()
            translated.pos = (
                event.pos[0] - self.panel_rect.x,
                event.pos[1] - self.panel_rect.y,
            )
            for control in self._controls:
                control.handle_event(translated)
        else:
            for control in self._controls:
                control.handle_event(event)

    def draw(self) -> None:
        """Draw the panel background, all controls, and the dividing line."""
        self.subsurface.fill(self.config.color_background)

        for control in self._controls:
            control.draw()

        pg.draw.line(
            self.surface,
            self.config.color_border,
            (self.divider_x, 0),
            (self.divider_x, self.panel_rect.height),
            self.config.border_width,
        )
