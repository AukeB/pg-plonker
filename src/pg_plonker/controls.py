"""Module for the stateful controls."""

import pygame as pg
from pygame import Surface

from pg_plonker import draw
from pg_plonker.gui_config_models import ButtonConfig, RGBColor, SliderConfig
from pg_plonker.utils import count_decimal_places

_config_button = ButtonConfig()
_config_slider = SliderConfig()


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
