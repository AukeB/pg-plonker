"""Module for the stateful controls.

Functions: - _create_font: Create a system font for a control.

Classes:
- Button: A stateful toggle button that delegates rendering to draw.button.
- Slider: A stateful horizontal slider that delegates rendering to draw.slider.
- Dropdown: A stateful dropdown that delegates rendering to the draw.dropdown
  functions.

Controls read the active style every time they are used, so a later set_style()
call changes existing controls too. Arguments given to a constructor are kept as
overrides until the next set_style() call.
"""

import pygame as pg
from pygame import Surface

from pg_plonker import draw
from pg_plonker.styles import get_style
from pg_plonker.styles.models import RGBColor
from pg_plonker.utils import count_decimal_places, resolve_override


def _create_font(font_name: str, font_size: int) -> pg.font.Font:
    """Create a system font for a control.

    Args:
        font_name (str): System font name, or a list of names separated by
            commas.
        font_size (int): Font size in points.

    Returns:
        font (pg.font.Font): The font object.
    """

    font = pg.font.SysFont(name=font_name, size=font_size)

    return font


class Button:
    """A stateful toggle button that delegates rendering to draw.button.

    Attributes:
        surface (Surface): The pygame surface the button is drawn onto.
        x (int): X-position of the button in pixels.
        y (int): Y-position of the button in pixels.
        text (str): Label rendered inside the button.
        border_width (int | None): Outer border thickness in pixels.
        border_width_inner (int | None): Inner border thickness in pixels.
        text_shadow_offset (int | None): Pixel offset of the text shadow.
        color_text (RGBColor | None): Color of the button text.
        color_border (RGBColor | None): Outer border color.
        color_border_inner_light (RGBColor | None): Light inner border color.
        color_border_inner_dark (RGBColor | None): Dark inner border color.
        color_text_shadow (RGBColor | None): Color of the text shadow.
        value (bool): Toggle state, True when active.

    Example:
        >>> screen = pg.display.set_mode((800, 600))
        >>> button = Button(surface=screen, x=20, y=20, text="Start")
        >>> button.draw()
        >>> button.value
        False
    """

    def __init__(
        self,
        surface: Surface,
        x: int,
        y: int,
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
    ) -> None:
        """Initialize a Button instance with rendering surface, position, and
        visual overrides.

        The Button is a stateful UI element that can toggle between active and
        inactive states. Any argument left as None follows the active style, and
        is read again each time the button is drawn.

        Args:
            surface (Surface): The pygame surface the button will be drawn onto.
            x (int): X-position of the button in pixels (screen or panel-local
                space).
            y (int): Y-position of the button in pixels (screen or panel-local
                space).
            width (int | None): Button width override in pixels.
            height (int | None): Button height override in pixels.
            text (str): Label rendered inside the button.
            font_name (str | None): System font name override.
            font_size (int | None): Font size override in points.
            border_width (int | None): Outer border thickness override in
                pixels.
            border_width_inner (int | None): Inner border thickness override.
            text_shadow_offset (int | None): Text shadow offset override in
                pixels.
            color_background_active (RGBColor | None): Background override when
                active.
            color_background_inactive (RGBColor | None): Background override
                when inactive.
            color_text (RGBColor | None): Color override of the button text.
            color_border (RGBColor | None): Outer border color override.
            color_border_inner_light (RGBColor | None): Light inner border color
                override.
            color_border_inner_dark (RGBColor | None): Dark inner border color
                override.
            color_text_shadow (RGBColor | None): Text shadow color override.
            value (bool): Initial toggle value of the button (False = inactive,
                True = active).
        """

        # Display.
        self.surface = surface
        self.x = x
        self.y = y
        self.text = text
        self._width = width
        self._height = height
        self._font_name = font_name
        self._font_size = font_size
        self._font: pg.font.Font | None = None
        self._font_key: tuple[str, int] | None = None
        self.border_width = border_width
        self.border_width_inner = border_width_inner
        self.text_shadow_offset = text_shadow_offset
        self._color_background_active = color_background_active
        self._color_background_inactive = color_background_inactive
        self.color_text = color_text
        self.color_border = color_border
        self.color_border_inner_light = color_border_inner_light
        self.color_border_inner_dark = color_border_inner_dark
        self.color_text_shadow = color_text_shadow

        # State.
        self.value = value
        self._pressed = False
        self._pointer_inside = False
        self._hovered = False

    @property
    def width(self) -> int:
        """Button width in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        width = resolve_override(self._width, style.button.width)

        return width

    @property
    def height(self) -> int:
        """Button height in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        height = resolve_override(self._height, style.button.height)

        return height

    @property
    def rect(self) -> pg.Rect:
        """The button's bounding rectangle, from its current size and position."""

        rect = pg.Rect(self.x, self.y, self.width, self.height)

        return rect

    @property
    def font(self) -> pg.font.Font:
        """The font for the label, recreated only when the font name or size
        changes.
        """

        style = get_style()
        font_name = resolve_override(self._font_name, style.button.font_name)
        font_size = resolve_override(self._font_size, style.button.font_size)
        font_key = (font_name, font_size)

        if self._font is None or self._font_key != font_key:
            self._font = _create_font(font_name=font_name, font_size=font_size)
            self._font_key = font_key

        return self._font

    def _background_color(self) -> RGBColor:
        """Return the background color for the current toggle state.

        Returns:
            color (RGBColor): The active or inactive background color.
        """

        style = get_style()

        if self.value:
            color = resolve_override(
                self._color_background_active, style.button.color_background_active
            )
        else:
            color = resolve_override(
                self._color_background_inactive, style.button.color_background_inactive
            )

        return color

    def draw(self) -> None:
        """Draw the button reflecting the toggle state, press state and hover."""

        style = get_style()
        hovered = self._hovered and style.hover
        pressed = self._pressed and self._pointer_inside and style.press_bevel
        color_background = self._background_color()

        draw.button(
            hovered=hovered,
            surface=self.surface,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            text=self.text,
            font=self.font,
            border_width=self.border_width,
            border_width_inner=self.border_width_inner,
            text_shadow_offset=self.text_shadow_offset,
            color_background=color_background,
            color_text=self.color_text,
            color_border=self.color_border,
            color_border_inner_light=self.color_border_inner_light,
            color_border_inner_dark=self.color_border_inner_dark,
            color_text_shadow=self.color_text_shadow,
            pressed=pressed,
        )

    def handle_event(self, event: pg.event.Event) -> None:
        """Track the press, toggle state on a release over the button, and show
        the pressed look only while the pointer is over the button.

        Moving the pointer off the button while it is held removes the pressed
        look, and moving back on restores it. The state toggles only if the
        mouse is released over the button.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._pressed = True
                self._pointer_inside = True

        if event.type == pg.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)

            if self._pressed:
                self._pointer_inside = self._hovered

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self._pressed and self.rect.collidepoint(event.pos):
                self.value = not self.value

            self._pressed = False
            self._pointer_inside = False


class Slider:
    """A stateful horizontal slider that delegates rendering to draw.slider.

    The slider is drawn inside a bevelled box with its label at the top, the
    value readout above the handle (when shown), and the track. The box height
    depends on whether the value is shown, so a slider with a value is taller.

    Attributes:
        surface (Surface): The pygame surface the slider is drawn onto.
        x (int): X-position of the track's left edge in pixels.
        y (int): Y-position of the track's vertical center in pixels.
        start (int | float): The minimum value of the range.
        stop (int | float): The maximum value of the range.
        step (int | float | None): Increment the value snaps to when dragging.
        border_width (int | None): Handle border thickness in pixels.
        show_value (bool): Whether the current value is drawn above the handle.
        text (str | None): Label drawn at the top of the box.
        value (int | float): The current value, within [start, stop].

    Example:
        >>> screen = pg.display.set_mode((800, 600))
        >>> slider = Slider(surface=screen, x=20, y=40, start=0, stop=10, value=5)
        >>> slider.draw()
        >>> slider.value
        5.0
    """

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
    ) -> None:
        """Initialize a Slider instance with rendering surface, track position,
        range, and visual overrides.

        Any argument left as None follows the active style, and is read again
        each time the slider is used.

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
                precision.
            width (int | None): Track length override in pixels.
            track_height (int | None): Track thickness override in pixels.
            handle_radius (int | None): Handle radius override in pixels.
            border_width (int | None): Handle border thickness override in
                pixels.
            font_name (str | None): System font name override.
            font_size (int | None): Font size override in points for the value.
            extra_decimal_places (int | None): Decimal places override added on
                top of the precision implied by start/stop/step.
            show_value (bool): Whether to render the current value above the
                handle.
            color_track (RGBColor | None): Track fill color override.
            color_track_filled (RGBColor | None): Color override of the filled
                portion of the track.
            color_handle (RGBColor | None): Handle fill color override.
            color_border (RGBColor | None): Handle border color override.
            color_text (RGBColor | None): Label and value readout color
                override.
            text (str | None): Label drawn at the top of the box. Pass None for
                no label.

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
        self._width = width
        self._track_height = track_height
        self._handle_radius = handle_radius
        self.border_width = border_width
        self._font_name = font_name
        self._font_size = font_size
        self._font: pg.font.Font | None = None
        self._font_key: tuple[str, int] | None = None
        self._label_font: pg.font.Font | None = None
        self._label_font_key: tuple[str, int] | None = None
        self._extra_decimal_places = extra_decimal_places
        self.show_value = show_value
        self.color_track = color_track
        self.color_track_filled = color_track_filled
        self.color_handle = color_handle
        self.color_border = color_border
        self.color_text = color_text
        self.text = text

        # State.
        self.value = round(value if value is not None else self.start, self._precision)
        self._dragging = False
        self._hovered = False

    @property
    def width(self) -> int:
        """Track length in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        width = resolve_override(self._width, style.slider.width)

        return width

    @property
    def track_height(self) -> int:
        """Track thickness in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        track_height = resolve_override(self._track_height, style.slider.height)

        return track_height

    @property
    def handle_radius(self) -> int:
        """Handle radius in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        handle_radius = resolve_override(
            self._handle_radius, style.slider.handle_radius
        )

        return handle_radius

    @property
    def padding(self) -> int:
        """Space between the box edge and its contents, from the style."""

        style = get_style()
        padding = style.slider.padding

        return padding

    @property
    def inset(self) -> int:
        """Horizontal room the box adds on each side of the track."""

        inset = self.padding + self.handle_radius

        return inset

    @property
    def font(self) -> pg.font.Font:
        """The font for the value readout, recreated only when the name or size
        changes.
        """

        style = get_style()
        font_name = resolve_override(self._font_name, style.slider.font_name)
        font_size = resolve_override(self._font_size, style.slider.font_size)
        font_key = (font_name, font_size)

        if self._font is None or self._font_key != font_key:
            self._font = _create_font(font_name=font_name, font_size=font_size)
            self._font_key = font_key

        return self._font

    @property
    def label_font(self) -> pg.font.Font:
        """The font for the label, recreated only when the name or size changes."""

        style = get_style()
        font_name = resolve_override(self._font_name, style.slider.font_name)
        font_size = style.slider.label_font_size
        font_key = (font_name, font_size)

        if self._label_font is None or self._label_font_key != font_key:
            self._label_font = _create_font(font_name=font_name, font_size=font_size)
            self._label_font_key = font_key

        return self._label_font

    @property
    def layout(self) -> draw.SliderLayout:
        """Where the label, value readout and track sit inside the box."""

        label_height = (
            self.label_font.size(self.text)[1] if self.text is not None else 0
        )
        readout_height = self.font.size("0")[1] if self.show_value else 0
        layout = draw.slider_layout(
            self.padding, self.handle_radius, label_height, readout_height
        )

        return layout

    @property
    def height(self) -> int:
        """Height of the box in pixels, which depends on whether the value is
        shown.
        """

        height = self.layout.height

        return height

    @property
    def rect(self) -> pg.Rect:
        """The box's bounding rectangle, from its position and current layout."""

        rect = pg.Rect(
            self.x - self.inset,
            self.y - self.layout.track_center,
            self.width + 2 * self.inset,
            self.height,
        )

        return rect

    @property
    def _precision(self) -> int:
        """Decimal places used to round values.

        The count comes from start, stop and step, plus a buffer, so dragged
        values stay free of floating-point noise while remaining readable.
        """

        style = get_style()
        extra_decimal_places = resolve_override(
            self._extra_decimal_places, style.slider.extra_decimal_places
        )
        start_decimals = count_decimal_places(self.start)
        stop_decimals = count_decimal_places(self.stop)
        step_decimals = count_decimal_places(self.step) if self.step is not None else 0
        largest_decimals = max(start_decimals, stop_decimals, step_decimals)
        precision = largest_decimals + extra_decimal_places

        return precision

    def place(self, left: int, top: int) -> None:
        """Position the box so its top-left corner is at the given point.

        Args:
            left (int): X-position of the box's left edge, in panel-local space.
            top (int): Y-position of the box's top edge, in panel-local space.
        """

        self.x = left + self.inset
        self.y = top + self.layout.track_center

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

        right_edge = self.x + self.width
        clamped_right = min(mouse_x, right_edge)
        clamped_x = max(self.x, clamped_right)
        fraction = (clamped_x - self.x) / self.width
        raw_value = self.start + fraction * (self.stop - self.start)

        if self.step is not None:
            steps_from_start = round((raw_value - self.start) / self.step)
            raw_value = self.start + steps_from_start * self.step

        value = round(raw_value, self._precision)
        capped_value = min(value, self.stop)
        value = max(self.start, capped_value)

        return value

    def draw(self) -> None:
        """Draw the box, label, value readout and track, with the handle's hover
        state.
        """

        style = get_style()
        hovered = self._hovered and style.hover

        draw.slider(
            surface=self.surface,
            x=self.x,
            y=self.y,
            start=self.start,
            stop=self.stop,
            value=self.value,
            precision=self._precision,
            width=self.width,
            height=self.track_height,
            handle_radius=self.handle_radius,
            border_width=self.border_width,
            font=self.font,
            show_value=self.show_value,
            color_track=self.color_track,
            color_track_filled=self.color_track_filled,
            color_handle=self.color_handle,
            hovered=hovered,
            color_border=self.color_border,
            color_text=self.color_text,
            text=self.text,
            label_font=self.label_font,
        )

    def handle_event(self, event: pg.event.Event) -> None:
        """Start, update, or stop a drag based on mouse events on the slider.

        A press anywhere on the slider (the handle or the track beside it) jumps
        the value to the mouse position and starts a drag. Once dragging, the
        value updates live on every mouse motion, and the drag ends on mouse
        release regardless of the release position.

        Args:
            event (pg.event.Event): The pygame event to handle.
        """

        handle_center = self._get_handle_center()
        handle_rect = pg.Rect(0, 0, self.handle_radius * 2, self.handle_radius * 2)
        handle_rect.center = handle_center

        track_band = pg.Rect(
            self.x,
            self.y - self.handle_radius,
            self.width,
            self.handle_radius * 2,
        )

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(event.pos) or track_band.collidepoint(
                event.pos
            ):
                self._dragging = True
                self.value = self._get_value_from_x(event.pos[0])

        if event.type == pg.MOUSEMOTION:
            self._hovered = handle_rect.collidepoint(event.pos)

        if event.type == pg.MOUSEMOTION and self._dragging:
            self.value = self._get_value_from_x(event.pos[0])

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False


class Dropdown:
    """A stateful dropdown/select control that delegates rendering to
    draw.dropdown_header and draw.dropdown_options.

    Attributes:
        surface (Surface): The pygame surface the dropdown is drawn onto.
        x (int): X-position of the header in pixels.
        y (int): Y-position of the header in pixels.
        options (list[str]): The selectable option labels, in display order.
        border_width (int | None): Outer border thickness in pixels.
        border_width_inner (int | None): Inner border thickness in pixels.
        text_shadow_offset (int | None): Pixel offset of the header's text
            shadow.
        arrow_size (int | None): Half-width and height of the arrow in pixels.
        color_text (RGBColor | None): Header and option text color.
        color_border (RGBColor | None): Outer and option border color.
        color_border_inner_light (RGBColor | None): Light inner border color.
        color_border_inner_dark (RGBColor | None): Dark inner border color.
        color_text_shadow (RGBColor | None): Color of the header's text shadow.
        color_arrow (RGBColor | None): Arrow indicator color.
        value (str): The selected option.
        is_open (bool): Whether the option list is open.

    Example:
        >>> screen = pg.display.set_mode((800, 600))
        >>> dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
        >>> dropdown.value
        'Easy'
        >>> dropdown.draw()
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
        options, and visual overrides.

        The Dropdown is a stateful UI element that holds a selected value from a
        fixed list of options. While closed, only the header is drawn and
        interactive. While open, the option list is meant to be drawn last (via
        `draw_options`) so it overlays other controls rather than pushing them
        down, and it captures clicks exclusively until it closes again.

        Any argument left as None follows the active style, and is read again
        each time the dropdown is used.

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
            width (int | None): Header/option width override in pixels.
            height (int | None): Header height override in pixels.
            option_height (int | None): Option row height override in pixels.
            font_name (str | None): System font name override.
            font_size (int | None): Font size override in points.
            border_width (int | None): Outer border thickness override in
                pixels.
            border_width_inner (int | None): Inner border thickness override.
            text_shadow_offset (int | None): Text shadow offset override in
                pixels.
            arrow_size (int | None): Arrow size override in pixels.
            color_background_active (RGBColor | None): Header background
                override while open.
            color_background_inactive (RGBColor | None): Header background
                override while closed.
            color_background_option (RGBColor | None): Option row background
                override.
            color_background_option_hover (RGBColor | None): Hovered option row
                background override.
            color_text (RGBColor | None): Header and option text color override.
            color_border (RGBColor | None): Outer/option border color override.
            color_border_inner_light (RGBColor | None): Light inner border color
                override.
            color_border_inner_dark (RGBColor | None): Dark inner border color
                override.
            color_text_shadow (RGBColor | None): Header text shadow color
                override.
            color_arrow (RGBColor | None): Arrow indicator color override.

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
        self._width = width
        self._height = height
        self._option_height = option_height
        self._font_name = font_name
        self._font_size = font_size
        self._font: pg.font.Font | None = None
        self._font_key: tuple[str, int] | None = None
        self.border_width = border_width
        self.border_width_inner = border_width_inner
        self.text_shadow_offset = text_shadow_offset
        self.arrow_size = arrow_size
        self._color_background_active = color_background_active
        self._color_background_inactive = color_background_inactive
        self.color_background_option = color_background_option
        self.color_background_option_hover = color_background_option_hover
        self.color_text = color_text
        self.color_border = color_border
        self.color_border_inner_light = color_border_inner_light
        self.color_border_inner_dark = color_border_inner_dark
        self.color_text_shadow = color_text_shadow
        self.color_arrow = color_arrow

        # State.
        self.value = value if value is not None else self.options[0]
        self.is_open = False
        self._pressed = False
        self._hovered_index: int | None = None
        self._header_hovered = False

    @property
    def width(self) -> int:
        """Header and option width in pixels: the override if given, otherwise
        the style value.
        """

        style = get_style()
        width = resolve_override(self._width, style.dropdown.width)

        return width

    @property
    def height(self) -> int:
        """Header height in pixels: the override if given, otherwise the style
        value.
        """

        style = get_style()
        height = resolve_override(self._height, style.dropdown.height)

        return height

    @property
    def option_height(self) -> int:
        """Option row height in pixels: the override if given, otherwise the
        style value.
        """

        style = get_style()
        option_height = resolve_override(
            self._option_height, style.dropdown.option_height
        )

        return option_height

    @property
    def rect(self) -> pg.Rect:
        """The header's bounding rectangle, from its current size and position."""

        rect = pg.Rect(self.x, self.y, self.width, self.height)

        return rect

    @property
    def font(self) -> pg.font.Font:
        """The font for the header and option labels, recreated only when the
        name or size changes.
        """

        style = get_style()
        font_name = resolve_override(self._font_name, style.dropdown.font_name)
        font_size = resolve_override(self._font_size, style.dropdown.font_size)
        font_key = (font_name, font_size)

        if self._font is None or self._font_key != font_key:
            self._font = _create_font(font_name=font_name, font_size=font_size)
            self._font_key = font_key

        return self._font

    def _header_background(self) -> RGBColor:
        """Return the header background for the current open state.

        Returns:
            color (RGBColor): The active color while open, otherwise the
                inactive color.
        """

        style = get_style()

        if self.is_open:
            color = resolve_override(
                self._color_background_active, style.dropdown.color_background_active
            )
        else:
            color = resolve_override(
                self._color_background_inactive,
                style.dropdown.color_background_inactive,
            )

        return color

    def _get_options_rect(self) -> pg.Rect:
        """Compute the bounding rect of the open option list.

        Returns:
            options_rect (pg.Rect): The rect covering all option rows, stacked
                directly below the header.
        """

        option_count = len(self.options)
        options_height = self.option_height * option_count

        options_rect = pg.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            options_height,
        )

        return options_rect

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

        style = get_style()
        hovered = self._header_hovered and style.hover
        color_background = self._header_background()

        draw.dropdown_header(
            surface=self.surface,
            x=self.x,
            y=self.y,
            text=self.value,
            is_open=self.is_open,
            width=self.width,
            height=self.height,
            font=self.font,
            border_width=self.border_width,
            border_width_inner=self.border_width_inner,
            text_shadow_offset=self.text_shadow_offset,
            arrow_size=self.arrow_size,
            color_background=color_background,
            hovered=hovered,
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
            font=self.font,
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

        if event.type == pg.MOUSEMOTION:
            self._header_hovered = self.rect.collidepoint(event.pos)

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
