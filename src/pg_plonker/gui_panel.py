"""Module for the UIPanel control container."""

import pygame as pg
from pygame import Rect, Surface

from pg_plonker.controls.button import Button
from pg_plonker.gui_config_models import GUIPanelConfig, RGBColor

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
        """Initialize a GUIPanel instance attached to a pygame surface.

        The GUIPanel represents a vertical UI container responsible for: - Defining a dedicated
        panel region within the main surface - Managing layout of child UI controls - Forwarding
        events to registered controls with coordinate translation - Rendering the panel background,
        divider, and all child controls

        Layout is computed immediately based on the provided surface size and alignment settings.
        The panel creates a subsurface to provide a local drawing coordinate space for contained
        controls.

        All configuration parameters are optional and fall back to values defined in
        `GUIPanelConfig` when not provided.

        Args:
            surface (Surface): The main pygame surface the panel is attached to.
            width (int | None): Width of the panel in pixels.
            border_width (int | None): Thickness of the divider line in pixels.
            margin_gui_panel (int | None): Top padding inside the panel.
            margin_button (int | None): Vertical spacing between controls.
            align_right (bool | None): If True, panel is anchored to the right side.
            color_background (RGBColor | None): Background fill color of the panel.
            color_border (RGBColor | None): Color of the divider line.
        """
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
        """Translate a screen-space pygame event into panel-local coordinates.

        This function converts global mouse coordinates into the panel's local coordinate space so
        that child controls can correctly perform hit- testing (e.g. collidepoint checks).

        Events occurring outside the panel bounds are ignored and return None.

        Args:
            event (pg.event.Event): A pygame event from the main event loop.

        Returns:
            pg.event.Event | None: A new event with translated coordinates if applicable, otherwise
                None if the event is outside the panel.
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
        """Create a Button, register it with the panel, and assign automatic layout.

        The button is created using the panel's subsurface so that it operates in panel- local
        coordinate space. Its final position is determined by the panel's layout system (vertical
        stacking with centering).

        The panel: - Instantiates the button with default or overridden styling - Assigns a computed
        x/y position based on layout rules - Updates internal layout cursor for subsequent controls
        - Registers the button for event handling and rendering

        Args:
            width (int | None): Button width in pixels.
            height (int | None): Button height in pixels.
            text (str | None): Label displayed inside the button.
            font_name (str | None): Font family used for rendering text.
            font_size (int | None): Font size in points.
            border_width (int | None): Outer border thickness.
            border_width_inner (int | None): Inner border thickness.
            text_shadow_offset (int | None): Shadow offset in pixels.
            color_background_active (RGBColor | None): Background color when active.
            color_background_inactive (RGBColor | None): Background color when inactive.
            color_text (RGBColor | None): Text color.
            color_border (RGBColor | None): Outer border color.
            color_border_inner_light (RGBColor | None): Inner light border color.
            color_border_inner_dark (RGBColor | None): Inner dark border color.
            color_text_shadow (RGBColor | None): Text shadow color.
            state (bool): Initial toggle state of the button.

        Returns:
            Button: The created and layout-managed button instance.
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
        """Forward a pygame event to all registered panel controls.

        Mouse events are first translated into panel-local coordinates before being dispatched,
        ensuring correct hit-testing within the panel's subsurface coordinate system.

        Non-mouse events are ignored if they fall outside the panel region.

        Args:
            event (pg.event.Event): Event from the pygame event queue.
        """
        translated = self._translate_event_to_local(event)

        if translated is None:
            return

        for control in self._controls:
            control.handle_event(translated)

    def draw(self) -> None:
        """Render the GUI panel and all contained controls.

        This includes: - Filling the panel background - Drawing all registered controls - Rendering
        the vertical divider line separating the panel from the main surface

        The panel uses a subsurface to ensure all child controls render in local coordinates,
        independent of the main surface coordinate space.
        """
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
