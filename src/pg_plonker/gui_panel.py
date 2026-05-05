"""Module for the UIPanel control container."""

import pygame as pg
from pygame import Rect, Surface

from src.pg_plonker.controls.button import Button
from src.pg_plonker.gui_config_models import GUIPanelConfig, RGBColor

_config_gui_panel = GUIPanelConfig()


class GUIPanel:
    """A side panel that owns and lays out stateful controls."""

    def __init__(
        self,
        surface: Surface,
        width: int | None = None,
        border_width: int | None = None,
        margin_gui_panel: int | None = None,
        margin_button: int | None = None,
        align_right: bool | None = None,
        color_background: RGBColor | None = None,
        color_border: RGBColor | None = None,
    ) -> None:
        """ """
        # Get all arguments, either from function input or config.
        self.surface = surface
        self.width = width or _config_gui_panel.width
        self.border_width = border_width or _config_gui_panel.border_width
        self.margin_gui_panel = margin_gui_panel or _config_gui_panel.margin_gui_panel
        self.margin_button = margin_button or _config_gui_panel.margin_button
        self.align_right = align_right or _config_gui_panel.align_right
        self.color_background = color_background or _config_gui_panel.color_background
        self.color_border = color_border or _config_gui_panel.color_border

        # Layout of the GUI Panel.
        screen_width, screen_height = surface.get_size()
        panel_x = screen_width - self.width if self.align_right else 0
        self.rect_panel = Rect(panel_x, 0, self.width, screen_height)
        self.subsurface = surface.subsurface(self.rect_panel)
        self.divider_x = panel_x if self.align_right else self.width

        # Controls.
        self._controls: list[Button] = []
        self._next_button_y = self.margin_gui_panel

    def _translate_event_to_local(self, event: pg.event.Event) -> pg.event.Event | None:
        """Convert a screen-space event into panel-local space.

        Returns None if the event is outside the panel.
        """
        if not hasattr(event, "pos"):
            return event

        if not self.rect_panel.collidepoint(event.pos):
            return None

        return pg.event.Event(
            event.type,
            {
                **event.dict,
                "pos": (
                    event.pos[0] - self.rect_panel.x,
                    event.pos[1] - self.rect_panel.y,
                ),
            },
        )

    def add_button(
        self,
        *,
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
    ) -> Button:
        """
        Create a button, register it with the panel, and automatically lay it out.
        """

        # Create a button. Use 0 for x and y position value. These values will get
        # overwritten because the button will get a predefined place in the UI-panel.
        button = Button(
            surface=self.subsurface,
            x=0,
            y=0,
            width=width,
            height=height,
            text=text,
            font_name=font_name,
            font_size=font_size,
            border_width=border_width,
            border_width_inner=border_width_inner,
            text_shadow_offset=text_shadow_offset,
            color_background_active=color_background_active,
            color_background_inactive=color_background_inactive,
            color_text=color_text,
            color_border=color_border,
            color_border_inner_light=color_border_inner_light,
            color_border_inner_dark=color_border_inner_dark,
            color_text_shadow=color_text_shadow,
            state=state,
        )

        button_x = (self.width - button.rect.width) // 2
        button_y = self._next_button_y
        button.x = button_x
        button.y = button_y

        # Assign final position (panel-local coords)
        button.rect = pg.Rect(
            button_x,
            button_y,
            button.rect.width,
            button.rect.height,
        )

        # Advance layout cursor for next GUI element that will be placed.
        self._next_button_y += button.rect.height + self.margin_button

        # Register control
        self._controls.append(button)

        return button

    def handle_event(self, event: pg.event.Event) -> None:
        translated = self._translate_event_to_local(event)

        if translated is None:
            return

        for control in self._controls:
            control.handle_event(translated)

    def draw(self) -> None:
        """Draw the panel background, all controls, and the dividing line."""
        self.subsurface.fill(self.color_background)

        for control in self._controls:
            control.draw()

        pg.draw.line(
            self.surface,
            self.color_border,
            (self.divider_x, 0),
            (self.divider_x, self.rect_panel.height),
            self.border_width,
        )
