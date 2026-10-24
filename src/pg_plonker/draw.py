"""Module for stateless pygame drawing functions for UI elements.

Functions:
- button: Draw a single button onto the given surface.
- slider: Draw a single horizontal slider onto the given surface.
- dropdown_header: Draw a single dropdown header onto the given surface.
- dropdown_options: Draw a dropdown's open option list onto the given surface.
"""

import pygame as pg
from pygame import Surface

from pg_plonker.styles import get_style
from pg_plonker.styles.models import RGBColor
from pg_plonker.utils import lighten_color


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
    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)

    # A pressed button reads as sunken, so its bevel light and dark swap.
    color_bevel_light = color_border_inner_light
    color_bevel_dark = color_border_inner_dark

    if pressed:
        color_bevel_light, color_bevel_dark = color_bevel_dark, color_bevel_light

    # Drawing operations.
    pg.draw.rect(surface, color_background, rect)
    pg.draw.rect(surface, color_border, rect, border_width)

    pg.draw.line(
        surface,
        color_bevel_light,
        inner_rect.topleft,
        inner_rect.topright,
        border_width_inner,
    )

    pg.draw.line(
        surface,
        color_bevel_light,
        inner_rect.topleft,
        inner_rect.bottomleft,
        border_width_inner,
    )

    pg.draw.line(
        surface,
        color_bevel_dark,
        inner_rect.bottomleft,
        inner_rect.bottomright,
        border_width_inner,
    )

    pg.draw.line(
        surface,
        color_bevel_dark,
        inner_rect.topright,
        inner_rect.bottomright,
        border_width_inner,
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
) -> None:
    """Draw a single horizontal slider onto the given surface.

    All parameters except surface, x, y, start, stop, value, and precision are
    optional and fall back to the active style when not provided. This allows
    quick usage with minimal arguments while still permitting per-call overrides
    of any visual property.

    Args:
        surface (Surface): The pygame surface to draw onto.
        x (int): X position of the track's left edge, in pixels.
        y (int): Y position of the track's vertical center, in pixels.
        start (int | float): The minimum value of the slider's range.
        stop (int | float): The maximum value of the slider's range.
        value (int | float): The current value, used to position the handle.
        precision (int): Number of decimal places to display when show_value is
            True.
        width (int | None): Track width in pixels, overrides config if provided.
        height (int | None): Track height in pixels, overrides config if
            provided.
        handle_radius (int | None): Handle circle radius in pixels, overrides
            config if provided.
        border_width (int | None): Handle border thickness in pixels, overrides
            config if provided.
        font (pg.font.Font): Font used to render the text.
        show_value (bool): Whether to render the current value above the handle.
        color_track (RGBColor | None): Track fill color, overrides config if
            provided.
        color_track_filled (RGBColor | None): Color of the filled portion of the
            track to the left of the handle, overrides config if provided.
        color_handle (RGBColor | None): Handle fill color, overrides config if
            provided.
        color_border (RGBColor | None): Handle border color, overrides config if
            provided.
        color_text (RGBColor | None): Value readout text color, overrides config
            if provided.
        hover_lighten (float | None): Fraction of the distance to white the
            handle moves while hovered, overrides config if provided.
        hovered (bool): Whether the pointer is over the handle. Defaults to
            False.
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

    # Definitions depending on function/config input.
    fraction = (value - start) / (stop - start)
    handle_x = x + int(fraction * width)
    handle_center = (handle_x, y)
    track_rect = pg.Rect(x, y - height // 2, width, height)
    track_filled_rect = pg.Rect(x, y - height // 2, handle_x - x, height)

    # Drawing operations.
    pg.draw.rect(surface, color_track, track_rect)
    pg.draw.rect(surface, color_track_filled, track_filled_rect)
    pg.draw.circle(surface, color_handle, handle_center, handle_radius)
    pg.draw.circle(surface, color_border, handle_center, handle_radius, border_width)

    if show_value:
        text_surface = font.render(f"{value:.{precision}f}", True, color_text)

        text_rect = text_surface.get_rect(
            midbottom=(handle_center[0], handle_center[1] - handle_radius - 4)
        )

        surface.blit(text_surface, text_rect)


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
    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)

    # Drawing operations.
    pg.draw.rect(surface, color_background, rect)
    pg.draw.rect(surface, color_border, rect, border_width)

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

    pg.draw.rect(surface, color_border, options_rect, border_width)
