"""Module for stateless pygame drawing functions for UI elements.

Functions:
- button: Draw a single button onto the given surface.
- slider: Draw a single horizontal slider onto the given surface.
- dropdown_header: Draw a single dropdown header onto the given surface.
- dropdown_options: Draw a dropdown's open option list onto the given surface.
"""

from typing import NamedTuple

import pygame as pg
from pygame import Surface

from pg_plonker.styles import get_style
from pg_plonker.styles.models import RGBColor
from pg_plonker.utils import lighten_color

# Gap in pixels between the top of the handle and the value readout above it.
_READOUT_GAP = 4

# Gap in pixels above and below the slider label.
_LABEL_GAP = 12


def _corner_radius(corner_radius: int | None) -> int:
    """Return the corner radius to draw with.

    Args:
        corner_radius (int | None): An explicit radius, or None to follow the
            active style.

    Returns:
        radius (int): The explicit radius if given. Otherwise the style's radius
            when the style is rounded, or 0 for square corners.
    """

    style = get_style()

    if corner_radius is not None:
        radius = corner_radius
    elif style.rounded:
        radius = style.corner_radius
    else:
        radius = 0

    return radius


def _draw_bevelled_box(
    surface: Surface,
    rect: pg.Rect,
    color_background: RGBColor,
    color_border: RGBColor,
    border_width: int,
    color_border_inner_light: RGBColor,
    color_border_inner_dark: RGBColor,
    border_width_inner: int,
    corner_radius: int = 0,
) -> None:
    """Draw a filled rectangle with an outer border and light/dark inner bevel.

    This is the same raised look the button uses.

    Args:
        surface (Surface): The pygame surface to draw onto.
        rect (pg.Rect): The box's rectangle.
        color_background (RGBColor): Fill colour.
        color_border (RGBColor): Outer border colour.
        border_width (int): Outer border thickness.
        color_border_inner_light (RGBColor): Light bevel colour.
        color_border_inner_dark (RGBColor): Dark bevel colour.
        border_width_inner (int): Inner bevel thickness.
        corner_radius (int): Corner radius in pixels, 0 for square corners.
    """

    pg.draw.rect(surface, color_background, rect, border_radius=corner_radius)
    if border_width > 0:
        pg.draw.rect(
            surface, color_border, rect, border_width, border_radius=corner_radius
        )

    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)
    pg.draw.line(
        surface,
        color_border_inner_light,
        inner_rect.topleft,
        inner_rect.topright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_light,
        inner_rect.topleft,
        inner_rect.bottomleft,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_dark,
        inner_rect.bottomleft,
        inner_rect.bottomright,
        border_width_inner,
    )
    pg.draw.line(
        surface,
        color_border_inner_dark,
        inner_rect.topright,
        inner_rect.bottomright,
        border_width_inner,
    )


def button(
    surface: Surface,
    x: int,
    y: int,
    font: pg.font.Font,
    width: int | None = None,
    height: int | None = None,
    text: str = "Button",
    border_width: int | None = None,
    border_width_inner: int | None = None,
    text_shadow_offset: int | None = None,
    color_background: RGBColor | None = None,
    color_text: RGBColor | None = None,
    color_border: RGBColor | None = None,
    color_border_inner_light: RGBColor | None = None,
    color_border_inner_dark: RGBColor | None = None,
    color_text_shadow: RGBColor | None = None,
    pressed: bool = False,
    hover_lighten: float | None = None,
    hovered: bool = False,
    corner_radius: int | None = None,
) -> None:
    """Draw a single button onto the given surface.

    All parameters except surface are optional and fall back to the values taken
    from the active style when not provided. This allows quick usage with
    minimal arguments while still permitting per-call overrides of any visual
    property.

    A pressed button swaps its inner bevel colors so it reads as sunken, without
    moving.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position in pixels.
        y (int): Y position in pixels.
        width (int | None): Button width in pixels, overrides config if
            provided.
        height (int | None): Button height in pixels, overrides config if
            provided.
        text (str | None): Label to render centered inside the button.
        font (pg.font.Font): Font used to render the text.
        border_width (int | None): Outer border thickness in pixels, overrides
            config if provided.
        border_width_inner (int | None): Inner border thickness in pixels,
            overrides config if provided.
        text_shadow_offset (int | None): Shadow offset in pixels, overrides
            config if provided.
        color_background (RGBColor | None): Background fill color, overrides
            config if provided.
        color_text (RGBColor | None): Text color, overrides config if provided.
        color_border (RGBColor | None): Outer border color, overrides config if
            provided.
        color_border_inner_light (RGBColor | None): Light inner border color,
            overrides config if provided.
        color_border_inner_dark (RGBColor | None): Dark inner border color,
            overrides config if provided.
        color_text_shadow (RGBColor | None): Text shadow color, overrides config
            if provided.
        pressed (bool): Whether the button is held down. Defaults to False.
        hover_lighten (float | None): Fraction of the distance to white the
            background moves while hovered, overrides config if provided.
        hovered (bool): Whether the pointer is over the button. Defaults to
            False.
    """

    # Get all arguments, either from function input or config.
    width = width if width is not None else get_style().button.width
    height = height if height is not None else get_style().button.height

    border_width = (
        border_width if border_width is not None else get_style().button.border_width
    )

    border_width_inner = (
        border_width_inner
        if border_width_inner is not None
        else get_style().button.border_width_inner
    )

    text_shadow_offset = (
        text_shadow_offset
        if text_shadow_offset is not None
        else get_style().button.text_shadow_offset
    )

    color_background = (
        color_background
        if color_background is not None
        else get_style().button.color_background_inactive
    )

    hover_lighten = (
        hover_lighten if hover_lighten is not None else get_style().hover_lighten
    )

    if hovered:
        color_background = lighten_color(color_background, hover_lighten)

    color_text = color_text if color_text is not None else get_style().button.color_text

    color_border = (
        color_border if color_border is not None else get_style().button.color_border
    )

    color_border_inner_light = (
        color_border_inner_light
        if color_border_inner_light is not None
        else get_style().button.color_border_inner_light
    )

    color_border_inner_dark = (
        color_border_inner_dark
        if color_border_inner_dark is not None
        else get_style().button.color_border_inner_dark
    )

    color_text_shadow = (
        color_text_shadow
        if color_text_shadow is not None
        else get_style().button.color_text_shadow
    )

    # Definitions depending on function/config input.
    rect = pg.Rect(x, y, width, height)
    # A pressed button reads as sunken, so its bevel light and dark swap.
    color_bevel_light = color_border_inner_light
    color_bevel_dark = color_border_inner_dark

    if pressed:
        color_bevel_light, color_bevel_dark = color_bevel_dark, color_bevel_light

    corner_radius = _corner_radius(corner_radius)

    # Drawing operations.
    _draw_bevelled_box(
        surface,
        rect,
        color_background,
        color_border,
        border_width,
        color_bevel_light,
        color_bevel_dark,
        border_width_inner,
        corner_radius,
    )

    shadow_surface = font.render(text, True, color_text_shadow)

    shadow_rect = shadow_surface.get_rect(
        center=(
            rect.centerx + text_shadow_offset,
            rect.centery + text_shadow_offset,
        )
    )

    surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


class SliderLayout(NamedTuple):
    """Vertical positions of a slider's parts, measured from the box's top edge.

    Attributes:
        height (int): Height of the box in pixels.
        track_center (int): Distance from the box's top to the track's centre.
        readout_top (int): Distance from the box's top to the value readout.
    """

    height: int
    track_center: int
    readout_top: int


def slider_layout(
    padding: int, handle_radius: int, label_height: int, readout_height: int
) -> SliderLayout:
    """Work out where a slider's label, value readout and track sit in its box.

    The label is at the top, then the value readout (when shown), then the
    track. Gaps are only added next to parts that are present, so a slider with
    no label or readout is no taller than its track needs.

    Args:
        padding (int): Space between the box edge and its contents.
        handle_radius (int): Handle radius, which sets the track's vertical
            room.
        label_height (int): Height of the label, or 0 when there is no label.
        readout_height (int): Height of the value readout, or 0 when not shown.

    Returns:
        layout (SliderLayout): The box height and the positions of its parts.
    """

    label_gap = _LABEL_GAP if label_height else 0
    readout_top = padding + label_height + label_gap
    readout_gap = _READOUT_GAP if readout_height else 0
    track_top = readout_top + readout_height + readout_gap
    track_center = track_top + handle_radius
    height = track_top + 2 * handle_radius + padding
    layout = SliderLayout(
        height=height, track_center=track_center, readout_top=readout_top
    )

    return layout


def slider(
    surface: Surface,
    x: int,
    y: int,
    start: int | float,
    stop: int | float,
    value: int | float,
    precision: int,
    font: pg.font.Font,
    width: int | None = None,
    height: int | None = None,
    handle_radius: int | None = None,
    border_width: int | None = None,
    show_value: bool = False,
    color_track: RGBColor | None = None,
    color_track_filled: RGBColor | None = None,
    color_handle: RGBColor | None = None,
    color_border: RGBColor | None = None,
    color_text: RGBColor | None = None,
    hover_lighten: float | None = None,
    hovered: bool = False,
    text: str | None = "Slider",
    label_font: pg.font.Font | None = None,
    padding: int | None = None,
    box_border_width: int | None = None,
    box_border_width_inner: int | None = None,
    color_box_background: RGBColor | None = None,
    color_box_border: RGBColor | None = None,
    color_box_border_inner_light: RGBColor | None = None,
    color_box_border_inner_dark: RGBColor | None = None,
    corner_radius: int | None = None,
) -> None:
    """Draw a single horizontal slider inside a bevelled box.

    The box holds the label (top), the value readout (when shown, above the
    handle) and the track. Its width is the track width plus the room the handle
    needs at each end. The box is drawn in the same style as a button.

    All parameters except surface, x, y, start, stop, value, and precision are
    optional and fall back to the active style when not provided.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position of the track's left edge, in pixels.
        y (int): Y position of the track's vertical center, in pixels.
        start (int | float): The minimum value of the slider's range.
        stop (int | float): The maximum value of the slider's range.
        value (int | float): The current value, used to position the handle.
        precision (int): Number of decimal places to display when show_value is
            True.
        width (int | None): Track width in pixels.
        height (int | None): Track thickness in pixels.
        handle_radius (int | None): Handle circle radius in pixels.
        border_width (int | None): Handle border thickness in pixels.
        font (pg.font.Font): Font used to render the value readout.
        show_value (bool): Whether to render the current value above the handle.
        color_track (RGBColor | None): Track fill color.
        color_track_filled (RGBColor | None): Color of the filled portion of the
            track to the left of the handle.
        color_handle (RGBColor | None): Handle fill color.
        color_border (RGBColor | None): Handle border color.
        color_text (RGBColor | None): Label and value readout text color.
        hover_lighten (float | None): Fraction of the distance to white the
            handle moves while hovered.
        hovered (bool): Whether the pointer is over the handle.
        text (str | None): Label drawn at the top of the box, aligned with the
            handle's left edge. Pass None to draw no label.
        label_font (pg.font.Font | None): Font for the label, defaults to font.
        padding (int | None): Space between the box edge and its contents.
        box_border_width (int | None): Outer border thickness of the box.
        box_border_width_inner (int | None): Inner bevel thickness of the box.
        color_box_background (RGBColor | None): Box background color.
        color_box_border (RGBColor | None): Box outer border color.
        color_box_border_inner_light (RGBColor | None): Box light bevel color.
        color_box_border_inner_dark (RGBColor | None): Box dark bevel color.
    """

    # Get all arguments, either from function input or config.
    width = width if width is not None else get_style().slider.width
    height = height if height is not None else get_style().slider.height

    handle_radius = (
        handle_radius if handle_radius is not None else get_style().slider.handle_radius
    )

    border_width = (
        border_width if border_width is not None else get_style().slider.border_width
    )

    color_track = (
        color_track if color_track is not None else get_style().slider.color_track
    )

    color_track_filled = (
        color_track_filled
        if color_track_filled is not None
        else get_style().slider.color_track_filled
    )

    color_handle = (
        color_handle if color_handle is not None else get_style().slider.color_handle
    )

    hover_lighten = (
        hover_lighten if hover_lighten is not None else get_style().hover_lighten
    )

    if hovered:
        color_handle = lighten_color(color_handle, hover_lighten)

    color_border = (
        color_border if color_border is not None else get_style().slider.color_border
    )

    color_text = color_text if color_text is not None else get_style().slider.color_text

    padding = padding if padding is not None else get_style().slider.padding

    box_border_width = (
        box_border_width
        if box_border_width is not None
        else get_style().slider.box_border_width
    )

    box_border_width_inner = (
        box_border_width_inner
        if box_border_width_inner is not None
        else get_style().slider.box_border_width_inner
    )

    color_box_background = (
        color_box_background
        if color_box_background is not None
        else get_style().slider.color_box_background
    )

    color_box_border = (
        color_box_border
        if color_box_border is not None
        else get_style().slider.color_box_border
    )

    color_box_border_inner_light = (
        color_box_border_inner_light
        if color_box_border_inner_light is not None
        else get_style().slider.color_box_border_inner_light
    )

    color_box_border_inner_dark = (
        color_box_border_inner_dark
        if color_box_border_inner_dark is not None
        else get_style().slider.color_box_border_inner_dark
    )

    label_font = label_font if label_font is not None else font
    label_height = label_font.size(text)[1] if text is not None else 0
    readout_height = font.size("0")[1] if show_value else 0

    # Definitions depending on function/config input.
    layout = slider_layout(padding, handle_radius, label_height, readout_height)
    inset = padding + handle_radius
    box_rect = pg.Rect(
        x - inset, y - layout.track_center, width + 2 * inset, layout.height
    )
    fraction = (value - start) / (stop - start)
    handle_x = x + int(fraction * width)
    handle_center = (handle_x, y)
    track_rect = pg.Rect(x, y - height // 2, width, height)
    track_filled_rect = pg.Rect(x, y - height // 2, handle_x - x, height)

    corner_radius = _corner_radius(corner_radius)
    track_radius = min(corner_radius, height // 2)

    # Drawing operations.
    _draw_bevelled_box(
        surface,
        box_rect,
        color_box_background,
        color_box_border,
        box_border_width,
        color_box_border_inner_light,
        color_box_border_inner_dark,
        box_border_width_inner,
        corner_radius,
    )
    pg.draw.rect(surface, color_track, track_rect, border_radius=track_radius)
    pg.draw.rect(
        surface, color_track_filled, track_filled_rect, border_radius=track_radius
    )
    pg.draw.circle(surface, color_handle, handle_center, handle_radius)
    if border_width > 0:
        pg.draw.circle(
            surface, color_border, handle_center, handle_radius, border_width
        )

    if show_value:
        text_surface = font.render(f"{value:.{precision}f}", True, color_text)
        readout_bottom = box_rect.y + layout.readout_top + readout_height
        text_rect = text_surface.get_rect(midbottom=(handle_x, readout_bottom))
        readout_area = pg.Rect(
            box_rect.x + padding,
            box_rect.y,
            box_rect.width - 2 * padding,
            box_rect.height,
        )
        text_rect.clamp_ip(readout_area)
        surface.blit(text_surface, text_rect)

    if text is not None:
        label_surface = label_font.render(text, True, color_text)
        label_rect = label_surface.get_rect(
            topleft=(box_rect.x + padding, box_rect.y + padding)
        )
        surface.blit(label_surface, label_rect)


def dropdown_header(
    surface: Surface,
    x: int,
    y: int,
    text: str,
    is_open: bool,
    font: pg.font.Font,
    width: int | None = None,
    height: int | None = None,
    border_width: int | None = None,
    border_width_inner: int | None = None,
    text_shadow_offset: int | None = None,
    arrow_size: int | None = None,
    text_padding: int | None = None,
    color_background: RGBColor | None = None,
    color_text: RGBColor | None = None,
    color_border: RGBColor | None = None,
    color_border_inner_light: RGBColor | None = None,
    color_border_inner_dark: RGBColor | None = None,
    color_text_shadow: RGBColor | None = None,
    color_arrow: RGBColor | None = None,
    hover_lighten: float | None = None,
    hovered: bool = False,
    corner_radius: int | None = None,
) -> None:
    """Draw a single dropdown header onto the given surface.

    The header reuses the same bevelled rect styling as `button` (outer border
    plus light/dark inner border lines) so a Dropdown reads as part of the same
    visual family. The selected option's text is left-aligned and shadowed the
    same way as Button labels, and an arrow indicator is drawn on the right,
    flipping between pointing down (closed) and up (open).

    All parameters except surface, x, y, text, and is_open are optional and fall
    back to the active style when not provided.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position in pixels.
        y (int): Y position in pixels.
        text (str): The currently selected option's label, rendered inside the
            header.
        is_open (bool): Whether the option list is currently open, controls the
            header's background color and arrow direction.
        width (int | None): Header width in pixels, overrides config if
            provided.
        height (int | None): Header height in pixels, overrides config if
            provided.
        font (pg.font.Font): Font used to render the text.
        border_width (int | None): Outer border thickness in pixels, overrides
            config if provided.
        border_width_inner (int | None): Inner border thickness in pixels,
            overrides config if provided.
        text_shadow_offset (int | None): Shadow offset in pixels, overrides
            config if provided.
        arrow_size (int | None): Half-width/height of the arrow indicator in
            pixels, overrides config if provided.
        text_padding (int | None): Space in pixels between the header edge and
            its label and arrow, overrides config if provided.
        color_background (RGBColor | None): Header background fill color,
            overrides config if provided.
        color_text (RGBColor | None): Text color, overrides config if provided.
        color_border (RGBColor | None): Outer border color, overrides config if
            provided.
        color_border_inner_light (RGBColor | None): Light inner border color,
            overrides config if provided.
        color_border_inner_dark (RGBColor | None): Dark inner border color,
            overrides config if provided.
        color_text_shadow (RGBColor | None): Text shadow color, overrides config
            if provided.
        color_arrow (RGBColor | None): Arrow indicator color, overrides config
            if provided.
        hover_lighten (float | None): Fraction of the distance to white the
            header background moves while hovered and closed, overrides config
            if provided.
        hovered (bool): Whether the pointer is over the header. Defaults to
            False.
    """

    # Get all arguments, either from function input or config.
    width = width if width is not None else get_style().dropdown.width
    height = height if height is not None else get_style().dropdown.height

    border_width = (
        border_width if border_width is not None else get_style().dropdown.border_width
    )

    border_width_inner = (
        border_width_inner
        if border_width_inner is not None
        else get_style().dropdown.border_width_inner
    )

    text_shadow_offset = (
        text_shadow_offset
        if text_shadow_offset is not None
        else get_style().dropdown.text_shadow_offset
    )

    arrow_size = (
        arrow_size if arrow_size is not None else get_style().dropdown.arrow_size
    )

    text_padding = (
        text_padding if text_padding is not None else get_style().dropdown.text_padding
    )

    color_background = (
        color_background
        if color_background is not None
        else (
            get_style().dropdown.color_background_active
            if is_open
            else get_style().dropdown.color_background_inactive
        )
    )

    hover_lighten = (
        hover_lighten if hover_lighten is not None else get_style().hover_lighten
    )

    if hovered and not is_open:
        color_background = lighten_color(color_background, hover_lighten)

    color_text = (
        color_text if color_text is not None else get_style().dropdown.color_text
    )

    color_border = (
        color_border if color_border is not None else get_style().dropdown.color_border
    )

    color_border_inner_light = (
        color_border_inner_light
        if color_border_inner_light is not None
        else get_style().dropdown.color_border_inner_light
    )

    color_border_inner_dark = (
        color_border_inner_dark
        if color_border_inner_dark is not None
        else get_style().dropdown.color_border_inner_dark
    )

    color_text_shadow = (
        color_text_shadow
        if color_text_shadow is not None
        else get_style().dropdown.color_text_shadow
    )

    color_arrow = (
        color_arrow if color_arrow is not None else get_style().dropdown.color_arrow
    )

    # Definitions depending on function/config input.
    rect = pg.Rect(x, y, width, height)

    # Drawing operations.
    _draw_bevelled_box(
        surface,
        rect,
        color_background,
        color_border,
        border_width,
        color_border_inner_light,
        color_border_inner_dark,
        border_width_inner,
        _corner_radius(corner_radius),
    )

    # Selected-option label, left-aligned with room reserved on the right for
    # the arrow.
    text_x = rect.x + border_width_inner * 2 + text_padding

    shadow_surface = font.render(text, True, color_text_shadow)

    shadow_rect = shadow_surface.get_rect(
        midleft=(text_x + text_shadow_offset, rect.centery + text_shadow_offset)
    )

    surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(midleft=(text_x, rect.centery))
    surface.blit(text_surface, text_rect)

    # Arrow indicator: points up while open, down while closed.
    arrow_x = rect.right - border_width_inner * 2 - text_padding - arrow_size
    arrow_y = rect.centery

    if is_open:
        arrow_points = [
            (arrow_x - arrow_size, arrow_y + arrow_size // 2),
            (arrow_x + arrow_size, arrow_y + arrow_size // 2),
            (arrow_x, arrow_y - arrow_size // 2),
        ]
    else:
        arrow_points = [
            (arrow_x - arrow_size, arrow_y - arrow_size // 2),
            (arrow_x + arrow_size, arrow_y - arrow_size // 2),
            (arrow_x, arrow_y + arrow_size // 2),
        ]

    pg.draw.polygon(surface, color_arrow, arrow_points)


def dropdown_options(
    surface: Surface,
    x: int,
    y: int,
    options: list[str],
    hovered_index: int | None,
    font: pg.font.Font,
    width: int | None = None,
    option_height: int | None = None,
    border_width: int | None = None,
    text_padding: int | None = None,
    color_background_option: RGBColor | None = None,
    color_background_option_hover: RGBColor | None = None,
    color_text: RGBColor | None = None,
    color_border: RGBColor | None = None,
) -> None:
    """Draw a dropdown's open option list onto the given surface.

    Options are stacked vertically starting directly below (x, y), each drawn as
    a bordered row containing a left-aligned label. This is meant to be called
    only while the owning Dropdown is open, and drawn after all other panel
    controls so the list overlays anything beneath it.

    All parameters except surface, x, y, options, and hovered_index are optional
    and fall back to the active style when not provided.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position of the option list's left edge, in pixels.
        y (int): Y position of the option list's top edge, in pixels (normally
            the bottom edge of the dropdown's header).
        options (list[str]): The labels to render, one per row, in order.
        hovered_index (int | None): Index of the currently hovered option, or
            None if no option is hovered. The corresponding row is drawn with
            the hover background color.
        width (int | None): Row width in pixels, overrides config if provided.
        option_height (int | None): Row height in pixels, overrides config if
            provided.
        font (pg.font.Font): Font used to render the text.
        border_width (int | None): Row border thickness in pixels, overrides
            config if provided.
        color_background_option (RGBColor | None): Default row background color,
            overrides config if provided.
        color_background_option_hover (RGBColor | None): Hovered row background
            color, overrides config if provided.
        color_text (RGBColor | None): Row label color, overrides config if
            provided.
        color_border (RGBColor | None): Row border color, overrides config if
            provided.
        text_padding (int | None): Space in pixels between the row's left edge
            and its label, overrides config if provided.
    """

    # Get all arguments, either from function input or config.
    width = width if width is not None else get_style().dropdown.width

    option_height = (
        option_height
        if option_height is not None
        else get_style().dropdown.option_height
    )

    border_width = (
        border_width if border_width is not None else get_style().dropdown.border_width
    )

    text_padding = (
        text_padding if text_padding is not None else get_style().dropdown.text_padding
    )

    color_background_option = (
        color_background_option
        if color_background_option is not None
        else get_style().dropdown.color_background_option
    )

    color_background_option_hover = (
        color_background_option_hover
        if color_background_option_hover is not None
        else get_style().dropdown.color_background_option_hover
    )

    color_text = (
        color_text if color_text is not None else get_style().dropdown.color_text
    )

    color_border = (
        color_border if color_border is not None else get_style().dropdown.color_border
    )

    # Drawing operations.
    for index, option_text in enumerate(options):
        row_rect = pg.Rect(x, y + index * option_height, width, option_height)

        color_background = (
            color_background_option_hover
            if index == hovered_index
            else color_background_option
        )

        pg.draw.rect(surface, color_background, row_rect)

        text_surface = font.render(option_text, True, color_text)
        text_rect = text_surface.get_rect(
            midleft=(row_rect.x + text_padding, row_rect.centery)
        )
        surface.blit(text_surface, text_rect)

    # Borders are drawn once for the whole list, so the lines between rows are
    # the same thickness as the outer edge instead of doubled by two rows.
    for index in range(1, len(options)):
        separator_rect = pg.Rect(x, y + index * option_height, width, border_width)

        pg.draw.rect(surface, color_border, separator_rect)

    # The outer top edge starts one border width above y, so it sits on top of
    # the header's bottom border instead of stacking below it.
    options_rect = pg.Rect(
        x,
        y - border_width,
        width,
        option_height * len(options) + border_width,
    )

    if border_width > 0:
        pg.draw.rect(surface, color_border, options_rect, border_width)
