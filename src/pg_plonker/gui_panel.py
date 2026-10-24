"""Module for the UIPanel control container.

Classes: - GUIPanel: A side panel that owns and lays out stateful controls.
"""

import pygame as pg
from pygame import Rect, Surface

from pg_plonker.controls import Button, Dropdown, Slider
from pg_plonker.styles import get_style
from pg_plonker.styles.models import RGBColor
from pg_plonker.utils import resolve_override


class GUIPanel:
    """A side panel that owns and lays out stateful controls.

    Attributes:
        surface (Surface): The main pygame surface the panel is attached to.
        width (int): Width of the panel in pixels.
        border_width (int): Thickness of the divider line in pixels.
        margin_gui_panel (int): Top padding inside the panel.
        margin_button (int): Vertical spacing between controls.
        align_right (bool): Whether the panel is anchored to the right edge.
        color_background (RGBColor): Background fill color of the panel.
        color_border (RGBColor): Color of the divider line.
        rect_panel (Rect): The panel's rectangle within the main surface.
        subsurface (Surface): The panel's local drawing surface.
        divider_x (int): Pixel column of the divider line.

    Example:
        >>> screen = pg.display.set_mode((1000, 700))
        >>> panel = GUIPanel(surface=screen)
        >>> grid_toggle = panel.add_button(text="Toggle Grid")
        >>> panel.handle_event(event)
        >>> panel.draw()
    """

    def __init__(
        self,
        surface: Surface,
        width: int = 620,
        border_width: int | None = None,
        margin_gui_panel: int = 40,
        margin_button: int = 24,
        align_right: bool = True,
        color_background: RGBColor | None = None,
        color_border: RGBColor | None = None,
    ) -> None:
        """Initialize a GUIPanel instance attached to a pygame surface.

        The GUIPanel represents a vertical UI container responsible for:
        - Defining a dedicated panel region within the main surface
        - Managing layout of child UI controls
        - Forwarding events to registered controls with coordinate translation
        - Rendering the panel background, divider, and all child controls

        Layout is computed immediately based on the provided surface size and
        alignment settings. The panel creates a subsurface to provide a local
        drawing coordinate space for contained controls.

        The layout arguments (width, margins, alignment) are plain values for
        this panel. The visual arguments (border width and colours) are
        overrides; any argument left as None follows the active style.

        Args:
            surface (Surface): The main pygame surface the panel is attached to.
            width (int): Width of the panel in pixels.
            border_width (int | None): Divider line thickness override in
                pixels.
            margin_gui_panel (int): Top padding inside the panel.
            margin_button (int): Vertical spacing between controls.
            align_right (bool): If True, panel is anchored to the right side.
            color_background (RGBColor | None): Background color override.
            color_border (RGBColor | None): Divider color override.
        """

        self.surface = surface
        self.width = width
        self._border_width = border_width
        self.margin_gui_panel = margin_gui_panel
        self.margin_button = margin_button
        self.align_right = align_right
        self._color_background = color_background
        self._color_border = color_border

        # Layout of the GUI Panel.
        screen_width, screen_height = surface.get_size()
        panel_x = screen_width - self.width if self.align_right else 0
        self.rect_panel = Rect(panel_x, 0, self.width, screen_height)
        self.subsurface = surface.subsurface(self.rect_panel)
        self.divider_x = panel_x if self.align_right else self.width

        # Controls.
        self._controls: list[Button | Slider | Dropdown] = []
        self._next_control_y = self.margin_gui_panel

    @property
    def border_width(self) -> int:
        """Divider thickness in pixels: the override if given, otherwise the
        style value.
        """

        style = get_style()
        border_width = resolve_override(self._border_width, style.panel.border_width)

        return border_width

    @property
    def color_background(self) -> RGBColor:
        """Panel background color: the override if given, otherwise the style
        value.
        """

        style = get_style()
        color_background = resolve_override(
            self._color_background, style.panel.color_background
        )

        return color_background

    @property
    def color_border(self) -> RGBColor:
        """Divider color: the override if given, otherwise the style value."""

        style = get_style()
        color_border = resolve_override(self._color_border, style.panel.color_border)

        return color_border

    def _translate_event_to_local(self, event: pg.event.Event) -> pg.event.Event:
        """Translate a screen-space pygame event into panel-local coordinates.

        This function converts global mouse coordinates into the panel's local
        coordinate space so that child controls can correctly perform hit-
        testing (e.g. collidepoint checks).

        Events outside the panel bounds are translated too, so their local
        position falls outside every control. Controls still need them, for
        example to end a press or drag when the mouse is released off the panel.

        Args:
            event (pg.event.Event): A pygame event from the main event loop.

        Returns:
            translated_event (pg.event.Event): The event with its position in
                panel-local coordinates, or the event unchanged if it has no
                position.
        """

        if not hasattr(event, "pos"):
            return event

        local_pos = (
            event.pos[0] - self.rect_panel.x,
            event.pos[1] - self.rect_panel.y,
        )

        local_attributes = {**event.dict, "pos": local_pos}
        translated_event = pg.event.Event(event.type, local_attributes)

        return translated_event

    def add_button(
        self,
        *,
        width: int | None = None,
        height: int | None = None,
        text: str = "Button",
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
        value: bool = False,
    ) -> Button:
        """Create a Button, register it with the panel, and assign automatic
        layout.

        The button is created using the panel's subsurface so that it operates
        in panel- local coordinate space. Its final position is determined by
        the panel's layout system (vertical stacking with centering).

        The panel:
        - Instantiates the button with default or overridden styling
        - Assigns a computed x/y position based on layout rules
        - Updates internal layout cursor for subsequent controls
        - Registers the button for event handling and rendering

        Args:
            width (int | None): Button width in pixels.
            height (int | None): Button height in pixels.
            text (str): Label displayed inside the button.
            font_name (str | None): Font family used for rendering text.
            font_size (int | None): Font size in points.
            border_width (int | None): Outer border thickness.
            border_width_inner (int | None): Inner border thickness.
            text_shadow_offset (int | None): Shadow offset in pixels.
            color_background_active (RGBColor | None): Background color when
                active.
            color_background_inactive (RGBColor | None): Background color when
                inactive.
            color_text (RGBColor | None): Text color.
            color_border (RGBColor | None): Outer border color.
            color_border_inner_light (RGBColor | None): Inner light border
                color.
            color_border_inner_dark (RGBColor | None): Inner dark border color.
            color_text_shadow (RGBColor | None): Text shadow color.
            value (bool): Initial toggle value of the button.

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
            value=value,
        )

        button_x = (self.width - button.rect.width) // 2
        button_y = self._next_control_y
        button.x = button_x
        button.y = button_y

        # Advance layout cursor for next GUI element that will be placed.
        self._next_control_y += button.rect.height + self.margin_button

        # Register control
        self._controls.append(button)

        return button

    def add_slider(
        self,
        *,
        start: int | float,
        stop: int | float,
        value: int | float | None = None,
        step: int | float | None = None,
        width: int | None = None,
        track_height: int | None = None,
        handle_radius: int | None = None,
        border_width: int | None = None,
        font_name: str | None = None,
        font_size: int | None = None,
        extra_decimal_places: int | None = None,
        show_value: bool = False,
        color_track: RGBColor | None = None,
        color_track_filled: RGBColor | None = None,
        color_handle: RGBColor | None = None,
        color_border: RGBColor | None = None,
        color_text: RGBColor | None = None,
        text: str | None = "Slider",
    ) -> Slider:
        """Create a Slider, register it with the panel, and assign automatic
        layout.

        The slider is created using the panel's subsurface so that it operates
        in panel-local coordinate space. Its final position is determined by the
        panel's layout system (vertical stacking with centering).

        The panel:
        - Instantiates the slider with default or overridden styling
        - Assigns a computed x/y position based on layout rules
        - Updates internal layout cursor for subsequent controls
        - Registers the slider for event handling and rendering

        Args:
            start (int | float): The minimum value of the slider's range.
            stop (int | float): The maximum value of the slider's range.
            value (int | float | None): Initial value, defaults to start if
                None.
            step (int | float | None): Increment the value snaps to when
                dragging. If None, the value is continuous.
            width (int | None): Track length in pixels.
            track_height (int | None): Track thickness in pixels.
            handle_radius (int | None): Handle circle radius in pixels.
            border_width (int | None): Handle border thickness in pixels.
            font_name (str | None): Font family used for the value readout.
            font_size (int | None): Font size in points.
            extra_decimal_places (int | None): Number of decimal places added on
                top of the precision already implied by start/stop.
            show_value (bool): Whether to render the current value above the
                handle.
            color_track (RGBColor | None): Track fill color.
            color_track_filled (RGBColor | None): Filled portion color.
            color_handle (RGBColor | None): Handle fill color.
            color_border (RGBColor | None): Handle border color.
            color_text (RGBColor | None): Value readout text color.
            text (str | None): Label drawn above the slider, starting at its
                left edge. Pass None for no label.

        Returns:
            Slider: The created and layout-managed slider instance.
        """

        # Create a slider. Use 0 for x and y position value. These values will
        # get overwritten because the slider will get a predefined place in
        # the UI-panel.
        slider = Slider(
            surface=self.subsurface,
            x=0,
            y=0,
            start=start,
            stop=stop,
            value=value,
            step=step,
            width=width,
            track_height=track_height,
            handle_radius=handle_radius,
            border_width=border_width,
            font_name=font_name,
            font_size=font_size,
            extra_decimal_places=extra_decimal_places,
            show_value=show_value,
            color_track=color_track,
            color_track_filled=color_track_filled,
            color_handle=color_handle,
            color_border=color_border,
            color_text=color_text,
            text=text,
        )

        slider_left = (self.width - slider.rect.width) // 2

        slider.place(left=slider_left, top=self._next_control_y)

        # Advance layout cursor for next GUI element that will be placed. The
        # slider's box is taller when its value is shown, so the next control
        # moves down by the box's own height.
        self._next_control_y += slider.height + self.margin_button

        # Register control
        self._controls.append(slider)

        return slider

    def add_dropdown(
        self,
        *,
        options: list[str],
        value: str | None = None,
        width: int | None = None,
        height: int | None = None,
        option_height: int | None = None,
        font_name: str | None = None,
        font_size: int | None = None,
        border_width: int | None = None,
        border_width_inner: int | None = None,
        text_shadow_offset: int | None = None,
        arrow_size: int | None = None,
        color_background_active: RGBColor | None = None,
        color_background_inactive: RGBColor | None = None,
        color_background_option: RGBColor | None = None,
        color_background_option_hover: RGBColor | None = None,
        color_text: RGBColor | None = None,
        color_border: RGBColor | None = None,
        color_border_inner_light: RGBColor | None = None,
        color_border_inner_dark: RGBColor | None = None,
        color_text_shadow: RGBColor | None = None,
        color_arrow: RGBColor | None = None,
    ) -> Dropdown:
        """Create a Dropdown, register it with the panel, and assign automatic
        layout.

        The dropdown is created using the panel's subsurface so that it operates
        in panel-local coordinate space. Its final position is determined by the
        panel's layout system (vertical stacking with centering). Only the
        closed header's height is reserved in the layout, since the open option
        list overlays other controls instead of displacing them.

        The panel:
        - Instantiates the dropdown with default or overridden styling
        - Assigns a computed x/y position based on layout rules
        - Updates internal layout cursor for subsequent controls
        - Registers the dropdown for event handling and rendering

        Args:
            options (list[str]): The selectable option labels, in display order.
            value (str | None): Initial selected value, defaults to the first
                option if None.
            width (int | None): Header/option width in pixels.
            height (int | None): Header height in pixels.
            option_height (int | None): Height of each option row in pixels.
            font_name (str | None): Font family used for rendering text.
            font_size (int | None): Font size in points.
            border_width (int | None): Outer border thickness.
            border_width_inner (int | None): Inner border thickness.
            text_shadow_offset (int | None): Shadow offset in pixels.
            arrow_size (int | None): Half-width/height of the arrow indicator.
            color_background_active (RGBColor | None): Header background color
                while open.
            color_background_inactive (RGBColor | None): Header background color
                while closed.
            color_background_option (RGBColor | None): Default option row
                background color.
            color_background_option_hover (RGBColor | None): Hovered option row
                background color.
            color_text (RGBColor | None): Header and option text color.
            color_border (RGBColor | None): Outer/option border color.
            color_border_inner_light (RGBColor | None): Inner light border
                color.
            color_border_inner_dark (RGBColor | None): Inner dark border color.
            color_text_shadow (RGBColor | None): Header text shadow color.
            color_arrow (RGBColor | None): Arrow indicator color.

        Returns:
            Dropdown: The created and layout-managed dropdown instance.
        """

        # Create a dropdown. Use 0 for x and y position value. These values
        # will get overwritten because the dropdown will get a predefined
        # place in the UI-panel.
        dropdown = Dropdown(
            surface=self.subsurface,
            x=0,
            y=0,
            options=options,
            value=value,
            width=width,
            height=height,
            option_height=option_height,
            font_name=font_name,
            font_size=font_size,
            border_width=border_width,
            border_width_inner=border_width_inner,
            text_shadow_offset=text_shadow_offset,
            arrow_size=arrow_size,
            color_background_active=color_background_active,
            color_background_inactive=color_background_inactive,
            color_background_option=color_background_option,
            color_background_option_hover=color_background_option_hover,
            color_text=color_text,
            color_border=color_border,
            color_border_inner_light=color_border_inner_light,
            color_border_inner_dark=color_border_inner_dark,
            color_text_shadow=color_text_shadow,
            color_arrow=color_arrow,
        )

        dropdown_x = (self.width - dropdown.rect.width) // 2
        dropdown_y = self._next_control_y
        dropdown.x = dropdown_x
        dropdown.y = dropdown_y

        # Advance layout cursor for next GUI element that will be placed. Only
        # the closed header's height is reserved: the open option list
        # overlays other controls (layout stays stable) rather than pushing
        # them down.
        self._next_control_y += dropdown.rect.height + self.margin_button

        # Register control
        self._controls.append(dropdown)

        return dropdown

    def handle_event(self, event: pg.event.Event) -> None:
        """Forward a pygame event to all registered panel controls.

        Mouse events are first translated into panel-local coordinates before
        being dispatched, ensuring correct hit-testing within the panel's
        subsurface coordinate system.

        Mouse events outside the panel are forwarded too, so a press or drag
        that started on a control ends when the mouse is released off the panel.
        Controls hit-test the local position themselves, so these events never
        trigger anything new.

        While a Dropdown's option list is open, it visually overlays the other
        controls, so it also takes exclusive ownership of events: other controls
        are not forwarded events until it closes again, preventing clicks on the
        option list from leaking through to whatever it's covering. The Dropdown
        closes itself on a click anywhere outside its list, including outside
        the panel.

        Args:
            event (pg.event.Event): Event from the pygame event queue.
        """

        open_dropdown_candidates = (
            control
            for control in self._controls
            if isinstance(control, Dropdown) and control.is_open
        )

        open_dropdown = next(open_dropdown_candidates, None)

        translated = self._translate_event_to_local(event)

        if open_dropdown is not None:
            open_dropdown.handle_event(translated)

            return

        for control in self._controls:
            control.handle_event(translated)

    def draw(self) -> None:
        """Render the GUI panel and all contained controls.

        This includes:
        - Filling the panel background
        - Drawing all registered controls
        - Rendering the vertical divider line separating the panel from the main
          surface

        The panel uses a subsurface to ensure all child controls render in local
        coordinates, independent of the main surface coordinate space.

        Any open Dropdown's option list is drawn in a second pass, after all
        other controls, so it overlays them instead of being drawn beneath.
        """

        self.subsurface.fill(self.color_background)

        for control in self._controls:
            control.draw()

        for control in self._controls:
            if isinstance(control, Dropdown):
                control.draw_options()

        pg.draw.line(
            self.surface,
            self.color_border,
            (self.divider_x, 0),
            (self.divider_x, self.rect_panel.height),
            self.border_width,
        )
