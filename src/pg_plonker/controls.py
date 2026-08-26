"""Module for the stateful controls."""

import pygame as pg
from pygame import Surface

from pg_plonker import draw
from pg_plonker.gui_config_models import (
    ButtonConfig,
    DropdownConfig,
    RGBColor,
    SliderConfig,
)
from pg_plonker.utils import count_decimal_places

_config_button = ButtonConfig()
_config_slider = SliderConfig()
_config_dropdown = DropdownConfig()


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
        value: bool = False,
    ) -> None:
        """Initialize a Button instance with rendering surface, position, and
        visual configuration.

        The Button is a stateful UI element that can toggle between active and
        inactive states. It stores its geometry and visual configuration and
        delegates rendering to the stateless `draw.button` function each frame.

        All visual parameters are optional and fall back to defaults defined in
        `ButtonConfig` when not provided.

        Args:
            surface (Surface): The pygame surface the button will be drawn onto.
            x (int): X-position of the button in pixels (screen or panel-local
                space).
            y (int): Y-position of the button in pixels (screen or panel-local
                space).
            width (int | None): Button width in pixels, defaults to config value
                if None.
            height (int | None): Button height in pixels, defaults to config
                value if None.
            text (str | None): Label rendered inside the button.
            font_name (str | None): System font name used for rendering text.
            font_size (int | None): Font size in points for button text.
            border_width (int | None): Outer border thickness in pixels.
            border_width_inner (int | None): Inner border thickness in pixels.
            text_shadow_offset (int | None): Pixel offset used for text shadow
                rendering.
            color_background_active (RGBColor | None): Background color when
                active.
            color_background_inactive (RGBColor | None): Background color when
                inactive.
            color_text (RGBColor | None): Color of the button text.
            color_border (RGBColor | None): Outer border color.
            color_border_inner_light (RGBColor | None): Light inner border
                highlight color.
            color_border_inner_dark (RGBColor | None): Dark inner border shadow
                color.
            color_text_shadow (RGBColor | None): Color of the text shadow.
            value (bool): Initial toggle value of the button (False = inactive,
                True = active).
        """
        # Display.
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width if width is not None else _config_button.width
        self.height = height if height is not None else _config_button.height
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.border_width = border_width
        self.border_width_inner = border_width_inner
        self.text_shadow_offset = text_shadow_offset
        self.color_background_active = (
            color_background_active
            if color_background_active is not None
            else _config_button.color_background_active
        )
        self.color_background_inactive = (
            color_background_inactive
            if color_background_inactive is not None
            else _config_button.color_background_inactive
        )
        self.color_text = color_text
        self.color_border = color_border
        self.color_border_inner_light = color_border_inner_light
        self.color_border_inner_dark = color_border_inner_dark
        self.color_text_shadow = color_text_shadow

        # Definitions depending on function/config input.
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        # State.
        self.value = value
        self._pressed = False

    def draw(self) -> None:
        """Draw the button reflecting the current toggle state."""
        color_background = (
            self.color_background_active
            if self.value
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

    def handle_event(self, event: pg.event.Event) -> None:
        """Toggle state on mouse release if the button was pressed down on this
        control.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._pressed = True

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self._pressed and self.rect.collidepoint(event.pos):
                self.value = not self.value

            self._pressed = False


class Slider:
    """A stateful horizontal slider that delegates rendering to draw.slider."""

    def __init__(
        self,
        surface: Surface,
        x: int,
        y: int,
        start: int | float,
        stop: int | float,
        value: int | float | None = None,
        step: int | float | None = None,
        width: int | None = None,
        height: int | None = None,
        handle_radius: int | None = None,
        border_width: int | None = None,
        margin_vertical: int | None = None,
        font_name: str | None = None,
        font_size: int | None = None,
        extra_decimal_places: int | None = None,
        show_value: bool = False,
        color_track: RGBColor | None = None,
        color_track_filled: RGBColor | None = None,
        color_handle: RGBColor | None = None,
        color_border: RGBColor | None = None,
        color_text: RGBColor | None = None,
    ) -> None:
        """Initialize a Slider instance with rendering surface, position, range,
        and visual configuration.

        The Slider is a stateful UI element that holds a numeric value within a
        fixed [start, stop] range. It stores its geometry, range, and visual
        configuration and delegates rendering to the stateless `draw.slider`
        function each frame.

        All visual parameters are optional and fall back to defaults defined in
        `SliderConfig` when not provided.

        Args:
            surface (Surface): The pygame surface the slider will be drawn onto.
            x (int): X-position of the track's left edge, in pixels (screen or
                panel-local space).
            y (int): Y-position of the track's vertical center, in pixels
                (screen or panel-local space).
            start (int | float): The minimum value of the slider's range.
            stop (int | float): The maximum value of the slider's range.
            value (int | float | None): Initial value, defaults to start if
                None.
            step (int | float | None): Increment the value snaps to when
                dragging. If None, the value is continuous, limited only by the
                configured decimal precision.
            width (int | None): Track width in pixels, defaults to config value
                if None.
            height (int | None): Track height in pixels, defaults to config
                value if None.
            handle_radius (int | None): Handle circle radius in pixels.
            border_width (int | None): Handle border thickness in pixels.
            margin_vertical (int | None): Vertical spacing reserved above and
                below the slider track when laid out in a GUIPanel, defaults to
                config value if None.
            font_name (str | None): System font name used for the value readout.
            font_size (int | None): Font size in points for the value readout.
            extra_decimal_places (int | None): Number of decimal places added on
                top of the precision already implied by start/stop.
            show_value (bool): Whether to render the current value above the
                handle.
            color_track (RGBColor | None): Track fill color.
            color_track_filled (RGBColor | None): Color of the filled portion of
                the track to the left of the handle.
            color_handle (RGBColor | None): Handle fill color.
            color_border (RGBColor | None): Handle border color.
            color_text (RGBColor | None): Value readout text color.

        Raises:
            ValueError: If start is not strictly less than stop, or if value
                falls outside the [start, stop] range.
        """
        if start >= stop:
            raise ValueError(f"start ({start}) must be less than stop ({stop}).")

        if value is not None and not (start <= value <= stop):
            raise ValueError(f"value ({value}) must be within [{start}, {stop}].")

        # Display.
        self.surface = surface
        self.x = x
        self.y = y
        self.start = start
        self.stop = stop
        self.step = step
        self.width = width if width is not None else _config_slider.width
        self.height = height if height is not None else _config_slider.height
        self.handle_radius = (
            handle_radius if handle_radius is not None else _config_slider.handle_radius
        )
        self.border_width = (
            border_width if border_width is not None else _config_slider.border_width
        )
        self.margin_vertical = (
            margin_vertical
            if margin_vertical is not None
            else _config_slider.margin_vertical
        )
        self.font_name = font_name
        self.font_size = font_size
        self.extra_decimal_places = (
            extra_decimal_places
            if extra_decimal_places is not None
            else _config_slider.extra_decimal_places
        )
        self.show_value = show_value
        self.color_track = color_track
        self.color_track_filled = color_track_filled
        self.color_handle = color_handle
        self.color_border = color_border
        self.color_text = color_text

        # Definitions depending on function/config input.
        self.rect = pg.Rect(self.x, self.y - self.height // 2, self.width, self.height)

        # The decimal count implied by start/stop/step, plus a buffer, so
        # dragged values stay free of floating-point noise while remaining
        # readable.
        self._precision = (
            max(
                count_decimal_places(self.start),
                count_decimal_places(self.stop),
                count_decimal_places(self.step) if self.step is not None else 0,
            )
            + self.extra_decimal_places
        )

        # State.
        self.value = round(value if value is not None else self.start, self._precision)
        self._dragging = False

    def _get_handle_center(self) -> tuple[int, int]:
        """Compute the current pixel center of the handle from self.value.

        Returns:
            handle_center (tuple[int, int]): The (x, y) pixel position of the
                handle's center.
        """
        fraction = (self.value - self.start) / (self.stop - self.start)
        handle_x = self.x + int(fraction * self.width)
        handle_center = (handle_x, self.y)

        return handle_center

    def _get_value_from_x(self, mouse_x: int) -> int | float:
        """Convert a pixel x-position into a value clamped to [start, stop].

        1. Clamp the x-position to the track's pixel bounds.
        2. Convert the clamped position into a [0, 1] fraction along the track.
        3. Map the fraction onto the [start, stop] range.
        4. Snap to the nearest step if one is configured.
        5. Round to the configured precision to remove floating-point noise.

        Args:
            mouse_x (int): The x-position of the mouse, in the same coordinate
                space as self.x.

        Returns:
            value (int | float): The resulting value, clamped to [start, stop].
        """
        clamped_x = max(self.x, min(mouse_x, self.x + self.width))
        fraction = (clamped_x - self.x) / self.width
        raw_value = self.start + fraction * (self.stop - self.start)

        if self.step is not None:
            steps_from_start = round((raw_value - self.start) / self.step)
            raw_value = self.start + steps_from_start * self.step

        value = round(raw_value, self._precision)
        value = max(self.start, min(value, self.stop))

        return value

    def draw(self) -> None:
        """Draw the slider reflecting the current value."""
        draw.slider(
            surface=self.surface,
            x=self.x,
            y=self.y,
            start=self.start,
            stop=self.stop,
            value=self.value,
            precision=self._precision,
            width=self.width,
            height=self.height,
            handle_radius=self.handle_radius,
            border_width=self.border_width,
            font_name=self.font_name,
            font_size=self.font_size,
            show_value=self.show_value,
            color_track=self.color_track,
            color_track_filled=self.color_track_filled,
            color_handle=self.color_handle,
            color_border=self.color_border,
            color_text=self.color_text,
        )

    def handle_event(self, event: pg.event.Event) -> None:
        """Start, update, or stop a drag based on mouse events near the handle.

        A drag starts only when the mouse is pressed down within the handle's
        bounding box (no click-to-jump on the track). Once dragging, the value
        updates live on every mouse motion, and the drag ends on mouse release
        regardless of the release position.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """
        handle_center = self._get_handle_center()
        handle_rect = pg.Rect(0, 0, self.handle_radius * 2, self.handle_radius * 2)
        handle_rect.center = handle_center

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(event.pos):
                self._dragging = True

        if event.type == pg.MOUSEMOTION and self._dragging:
            self.value = self._get_value_from_x(event.pos[0])

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False


class Dropdown:
    """A stateful dropdown/select control that delegates rendering to
    draw.dropdown_header and draw.dropdown_options.
    """

    def __init__(
        self,
        surface: Surface,
        x: int,
        y: int,
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
    ) -> None:
        """Initialize a Dropdown instance with rendering surface, position,
        options, and visual configuration.

        The Dropdown is a stateful UI element that holds a selected value from a
        fixed list of options. While closed, only the header is drawn and
        interactive. While open, the option list is meant to be drawn last (via
        `draw_options`) so it overlays other controls rather than pushing them
        down, and it captures clicks exclusively until it closes again.

        All visual parameters are optional and fall back to defaults defined in
        `DropdownConfig` when not provided.

        Args:
            surface (Surface): The pygame surface the dropdown will be drawn
                onto.
            x (int): X-position of the header in pixels (screen or panel-local
                space).
            y (int): Y-position of the header in pixels (screen or panel-local
                space).
            options (list[str]): The selectable option labels, in display order.
            value (str | None): Initial selected value, defaults to the first
                option if None.
            width (int | None): Header/option width in pixels, defaults to
                config value if None.
            height (int | None): Header height in pixels, defaults to config
                value if None.
            option_height (int | None): Height of each option row in pixels,
                defaults to config value if None.
            font_name (str | None): System font name used for rendering text.
            font_size (int | None): Font size in points for header/option text.
            border_width (int | None): Outer border thickness in pixels.
            border_width_inner (int | None): Inner border thickness in pixels.
            text_shadow_offset (int | None): Pixel offset used for the header's
                text shadow rendering.
            arrow_size (int | None): Half-width/height of the arrow indicator in
                pixels.
            color_background_active (RGBColor | None): Header background color
                while open.
            color_background_inactive (RGBColor | None): Header background color
                while closed.
            color_background_option (RGBColor | None): Default option row
                background color.
            color_background_option_hover (RGBColor | None): Hovered option row
                background color.
            color_text (RGBColor | None): Color of the header and option text.
            color_border (RGBColor | None): Outer/option border color.
            color_border_inner_light (RGBColor | None): Light inner border
                highlight color.
            color_border_inner_dark (RGBColor | None): Dark inner border shadow
                color.
            color_text_shadow (RGBColor | None): Color of the header's text
                shadow.
            color_arrow (RGBColor | None): Arrow indicator color.

        Raises:
            ValueError: If options is empty, or if value is provided but is not
                one of options.
        """
        if not options:
            raise ValueError("options must not be empty.")

        if value is not None and value not in options:
            raise ValueError(f"value ({value!r}) must be one of {options}.")

        # Display.
        self.surface = surface
        self.x = x
        self.y = y
        self.options = options
        self.width = width if width is not None else _config_dropdown.width
        self.height = height if height is not None else _config_dropdown.height
        self.option_height = (
            option_height
            if option_height is not None
            else _config_dropdown.option_height
        )
        self.font_name = font_name
        self.font_size = font_size
        self.border_width = border_width
        self.border_width_inner = border_width_inner
        self.text_shadow_offset = text_shadow_offset
        self.arrow_size = arrow_size
        self.color_background_active = (
            color_background_active
            if color_background_active is not None
            else _config_dropdown.color_background_active
        )
        self.color_background_inactive = (
            color_background_inactive
            if color_background_inactive is not None
            else _config_dropdown.color_background_inactive
        )
        self.color_background_option = color_background_option
        self.color_background_option_hover = color_background_option_hover
        self.color_text = color_text
        self.color_border = color_border
        self.color_border_inner_light = color_border_inner_light
        self.color_border_inner_dark = color_border_inner_dark
        self.color_text_shadow = color_text_shadow
        self.color_arrow = color_arrow

        # Definitions depending on function/config input.
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        # State.
        self.value = value if value is not None else self.options[0]
        self.is_open = False
        self._pressed = False
        self._hovered_index: int | None = None

    def _get_options_rect(self) -> pg.Rect:
        """Compute the bounding rect of the open option list.

        Returns:
            options_rect (pg.Rect): The rect covering all option rows, stacked
                directly below the header.
        """
        return pg.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            self.option_height * len(self.options),
        )

    def close(self) -> None:
        """Close the option list without changing the selected value.

        Safe to call whether or not the dropdown is currently open, so callers
        (e.g. the owning panel handling an outside click) don't need to check
        `is_open` first.
        """
        self.is_open = False
        self._hovered_index = None

    def draw(self) -> None:
        """Draw the dropdown header reflecting the current selection and open
        state.

        This does not draw the option list even while open; call `draw_options`
        separately, after all other controls, so the list overlays them instead
        of being drawn beneath.
        """
        draw.dropdown_header(
            surface=self.surface,
            x=self.x,
            y=self.y,
            text=self.value,
            is_open=self.is_open,
            width=self.width,
            height=self.height,
            font_name=self.font_name,
            font_size=self.font_size,
            border_width=self.border_width,
            border_width_inner=self.border_width_inner,
            text_shadow_offset=self.text_shadow_offset,
            arrow_size=self.arrow_size,
            color_background=(
                self.color_background_active
                if self.is_open
                else self.color_background_inactive
            ),
            color_text=self.color_text,
            color_border=self.color_border,
            color_border_inner_light=self.color_border_inner_light,
            color_border_inner_dark=self.color_border_inner_dark,
            color_text_shadow=self.color_text_shadow,
            color_arrow=self.color_arrow,
        )

    def draw_options(self) -> None:
        """Draw the open option list, overlaying anything beneath it.

        This is a no-op while the dropdown is closed. Callers should invoke this
        after drawing all other controls so the option list is not drawn over by
        them.
        """
        if not self.is_open:
            return

        draw.dropdown_options(
            surface=self.surface,
            x=self.rect.x,
            y=self.rect.bottom,
            options=self.options,
            hovered_index=self._hovered_index,
            width=self.width,
            option_height=self.option_height,
            font_name=self.font_name,
            font_size=self.font_size,
            border_width=self.border_width,
            color_background_option=self.color_background_option,
            color_background_option_hover=self.color_background_option_hover,
            color_text=self.color_text,
            color_border=self.color_border,
        )

    def handle_event(self, event: pg.event.Event) -> None:
        """Open, close, select, or hover based on mouse events.

        While closed, the header toggles open on mouse release if it was pressed
        down on this control (mirroring Button). While open, mouse motion
        updates the hovered option row, and a mouse press either selects the
        option under the cursor (if any) or simply closes the list, since
        clicking an option or clicking anywhere outside the list should both
        close it.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """
        if self.is_open:
            options_rect = self._get_options_rect()

            if event.type == pg.MOUSEMOTION:
                if options_rect.collidepoint(event.pos):
                    self._hovered_index = (
                        event.pos[1] - options_rect.y
                    ) // self.option_height
                else:
                    self._hovered_index = None

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if options_rect.collidepoint(event.pos):
                    index = (event.pos[1] - options_rect.y) // self.option_height
                    self.value = self.options[index]

                self.close()

        else:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self._pressed = True

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self._pressed and self.rect.collidepoint(event.pos):
                    self.is_open = True

                self._pressed = False
