"""Tests for the draw module."""

import pygame as pg

from pg_plonker import draw
from pg_plonker.styles import set_style

# Testing the "button" function.


def test_button_fills_background_with_given_color(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.button(surface=screen, font=font, x=20, y=20, color_background=(10, 20, 30))

    pixel = screen.get_at((20 + 540 - 30, 20 + 54))

    assert tuple(pixel)[:3] == (10, 20, 30)


def test_button_uses_style_defaults_when_no_overrides(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.button(surface=screen, font=font, x=20, y=20)

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


def test_button_hovered_lightens_background(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_background=(100, 100, 100),
        hover_lighten=0.2,
        hovered=True,
    )

    background = screen.get_at((20 + 100, 20 + 20))

    assert tuple(background)[:3] == (131, 131, 131)


def test_button_pressed_does_not_move_the_button(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_background=(10, 20, 30),
        color_border=(0, 0, 0),
        pressed=True,
    )

    top_left_corner = screen.get_at((20 + 1, 20 + 1))
    background_middle = screen.get_at((20 + 100, 20 + 20))

    assert tuple(top_left_corner)[:3] == (0, 0, 0)
    assert tuple(background_middle)[:3] == (10, 20, 30)


def test_button_pressed_swaps_bevel_colors(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_border_inner_light=(1, 1, 1),
        color_border_inner_dark=(2, 2, 2),
    )

    unpressed_light_bevel = screen.get_at((20 + 100, 20 + 6))

    screen.fill((0, 0, 0))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_border_inner_light=(1, 1, 1),
        color_border_inner_dark=(2, 2, 2),
        pressed=True,
    )

    pressed_light_bevel = screen.get_at((20 + 100, 20 + 6))

    assert tuple(unpressed_light_bevel)[:3] == (1, 1, 1)
    assert tuple(pressed_light_bevel)[:3] == (2, 2, 2)


# Testing the "slider" function.


def test_slider_draws_the_filled_part_up_to_the_handle(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.slider(
        surface=screen,
        font=font,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=10,
        precision=1,
        color_track_filled=(200, 10, 10),
    )

    pixel = screen.get_at((20 + 10, 100))

    assert tuple(pixel)[:3] == (200, 10, 10)


def test_slider_shows_value_when_requested(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.slider(
        surface=screen,
        font=font,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=3.5,
        precision=2,
        show_value=True,
    )

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


# Testing the "dropdown_header" function.


def test_slider_handle_hovered_lightens_handle(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        width=540,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=5,
        precision=1,
        color_handle=(100, 100, 100),
        hover_lighten=0.2,
        hovered=True,
    )

    handle = screen.get_at((20 + 270, 100))

    assert tuple(handle)[:3] == (131, 131, 131)


def test_dropdown_header_draws_closed_and_open_states(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_header(
        surface=screen, font=font, x=20, y=20, text="Easy", is_open=False
    )

    closed_average = pg.transform.average_color(screen)[:3]

    screen.fill((0, 0, 0))

    draw.dropdown_header(
        surface=screen, font=font, x=20, y=20, text="Easy", is_open=True
    )

    open_average = pg.transform.average_color(screen)[:3]

    assert closed_average != (0, 0, 0)
    assert open_average != (0, 0, 0)


def test_dropdown_header_hovered_lightens_background(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.dropdown_header(
        surface=screen,
        font=font,
        x=20,
        y=20,
        text="Easy",
        is_open=False,
        color_background=(100, 100, 100),
        hover_lighten=0.2,
        hovered=True,
    )

    background = screen.get_at((20 + 270, 20 + 20))

    assert tuple(background)[:3] == (131, 131, 131)


# Testing the "dropdown_options" function.


def test_dropdown_options_paints_the_hovered_row(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy", "Hard"],
        hovered_index=1,
        color_background_option_hover=(5, 6, 7),
    )

    pixel = screen.get_at((20 + 540 - 30, 100 + 60 + 30))

    assert tuple(pixel)[:3] == (5, 6, 7)


def test_dropdown_options_without_hover_uses_default_color(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy"],
        hovered_index=None,
        color_background_option=(8, 9, 10),
    )

    pixel = screen.get_at((20 + 540 - 30, 100 + 30))

    assert tuple(pixel)[:3] == (8, 9, 10)


def test_dropdown_options_separator_is_border_width_thick(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy", "Hard"],
        hovered_index=None,
        width=200,
        option_height=60,
        border_width=2,
        color_background_option=(8, 9, 10),
        color_border=(1, 2, 3),
    )

    above_separator = screen.get_at((20 + 100, 100 + 59))
    first_separator_row = screen.get_at((20 + 100, 100 + 60))
    second_separator_row = screen.get_at((20 + 100, 100 + 61))
    below_separator = screen.get_at((20 + 100, 100 + 62))

    assert tuple(above_separator)[:3] == (8, 9, 10)
    assert tuple(first_separator_row)[:3] == (1, 2, 3)
    assert tuple(second_separator_row)[:3] == (1, 2, 3)
    assert tuple(below_separator)[:3] == (8, 9, 10)


def test_dropdown_options_outer_border_is_border_width_thick(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy", "Hard"],
        hovered_index=None,
        width=200,
        option_height=60,
        border_width=2,
        color_background_option=(8, 9, 10),
        color_border=(1, 2, 3),
    )

    left_edge = screen.get_at((20, 100 + 30))
    inside_left_edge = screen.get_at((20 + 2, 100 + 30))

    assert tuple(left_edge)[:3] == (1, 2, 3)
    assert tuple(inside_left_edge)[:3] == (8, 9, 10)


def test_dropdown_options_top_border_overlaps_header_bottom_border(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy", "Hard"],
        hovered_index=None,
        width=200,
        option_height=60,
        border_width=2,
        color_background_option=(8, 9, 10),
        color_border=(1, 2, 3),
    )

    header_bottom_border = screen.get_at((20 + 100, 100 - 2))
    header_bottom_border_inner = screen.get_at((20 + 100, 100 - 1))
    first_row = screen.get_at((20 + 100, 100))

    assert tuple(header_bottom_border)[:3] == (1, 2, 3)
    assert tuple(header_bottom_border_inner)[:3] == (1, 2, 3)
    assert tuple(first_row)[:3] == (8, 9, 10)


def test_slider_text_is_drawn_above_the_track_at_its_left_edge(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        label_font=font,
        text="Speed",
        width=540,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=5,
        precision=1,
    )

    label_pixels = [
        (x, y)
        for x in range(0, 200)
        for y in range(40, 90)
        if tuple(screen.get_at((x, y)))[:3] != (255, 255, 255)
    ]

    assert label_pixels
    assert min(x for x, _ in label_pixels) <= 20 - 16 + 3


def test_slider_label_is_drawn_above_the_value_readout(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        label_font=font,
        text="Speed",
        show_value=True,
        width=540,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=5,
        precision=1,
        color_box_background=(255, 255, 255),
        color_box_border=(255, 255, 255),
        color_box_border_inner_light=(255, 255, 255),
        color_box_border_inner_dark=(255, 255, 255),
    )

    label_pixels = [
        (x, y)
        for x in range(20, 120)
        for y in range(40, 90)
        if tuple(screen.get_at((x, y)))[:3] != (255, 255, 255)
    ]

    assert label_pixels
    assert max(y for _, y in label_pixels) < 100 - 16


def test_slider_with_no_text_draws_no_label(screen: pg.Surface, font: pg.font.Font) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        text=None,
        width=540,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=5,
        precision=1,
        color_box_background=(255, 255, 255),
        color_box_border=(255, 255, 255),
        color_box_border_inner_light=(255, 255, 255),
        color_box_border_inner_dark=(255, 255, 255),
    )

    label_region = [
        screen.get_at((x, y)) for x in range(20, 120) for y in range(40, 90)
    ]

    assert all(tuple(pixel)[:3] == (255, 255, 255) for pixel in label_region)


def test_slider_value_readout_stays_inside_the_box_padding_at_the_left_end(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))
    padding = 4
    handle_radius = 10
    box_left = 20 - handle_radius - padding

    draw.slider(
        surface=screen,
        font=font,
        width=300,
        height=12,
        handle_radius=handle_radius,
        padding=padding,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=0,
        precision=2,
        show_value=True,
        text=None,
        color_text=(0, 0, 0),
        color_box_background=(255, 255, 255),
        color_box_border=(255, 255, 255),
        color_box_border_inner_light=(255, 255, 255),
        color_box_border_inner_dark=(255, 255, 255),
        box_border_width=0,
        box_border_width_inner=0,
    )

    readout_pixels = [
        x
        for x in range(0, 200)
        for y in range(0, 90)
        if tuple(screen.get_at((x, y)))[:3] == (0, 0, 0)
    ]

    assert readout_pixels
    assert min(readout_pixels) >= box_left + padding


def test_button_with_zero_border_width_draws_no_outline(screen: pg.Surface, font: pg.font.Font) -> None:
    screen.fill((255, 255, 255))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_background=(10, 20, 30),
        color_border=(0, 0, 0),
        border_width=0,
        border_width_inner=0,
    )

    edge = screen.get_at((20 + 1, 20 + 54))

    assert tuple(edge)[:3] == (10, 20, 30)


def test_slider_handle_with_zero_border_width_draws_no_outline(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        width=300,
        height=12,
        handle_radius=10,
        border_width=0,
        color_handle=(240, 240, 240),
        color_border=(0, 0, 0),
        x=20,
        y=100,
        start=0,
        stop=10,
        value=5,
        precision=1,
        text=None,
    )

    handle_edge = screen.get_at((20 + 150 + 8, 100))

    assert tuple(handle_edge)[:3] == (240, 240, 240)


def test_dropdown_options_with_zero_border_width_draws_no_frame(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.dropdown_options(
        surface=screen,
        font=font,
        x=20,
        y=100,
        options=["Easy"],
        hovered_index=None,
        width=200,
        option_height=60,
        border_width=0,
        color_background_option=(8, 9, 10),
        color_border=(0, 0, 0),
    )

    frame_edge = screen.get_at((20, 100 + 30))

    assert tuple(frame_edge)[:3] == (8, 9, 10)


def test_button_with_corner_radius_leaves_the_corner_unfilled(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_background=(10, 20, 30),
        color_border=(0, 0, 0),
        border_width=0,
        border_width_inner=0,
        corner_radius=10,
    )

    assert tuple(screen.get_at((20, 20)))[:3] == (255, 255, 255)
    assert tuple(screen.get_at((20 + 54, 20)))[:3] == (10, 20, 30)


def test_button_rounds_its_corners_when_the_active_style_is_rounded(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))
    set_style("chalk")
    try:
        draw.button(
            surface=screen,
            font=font,
            x=20,
            y=20,
            color_background=(10, 20, 30),
            border_width=0,
            border_width_inner=0,
        )
        corner = screen.get_at((20, 20))
    finally:
        set_style("embossed")

    assert tuple(corner)[:3] == (255, 255, 255)


def test_slider_track_ends_are_rounded_when_corner_radius_is_given(
    screen: pg.Surface, font: pg.font.Font
) -> None:
    screen.fill((255, 255, 255))

    draw.slider(
        surface=screen,
        font=font,
        width=300,
        height=12,
        handle_radius=10,
        color_track=(200, 200, 200),
        color_track_filled=(10, 20, 30),
        color_box_background=(255, 255, 255),
        box_border_width=0,
        box_border_width_inner=0,
        corner_radius=6,
        x=20,
        y=100,
        start=0,
        stop=10,
        value=10,
        precision=1,
        text=None,
    )

    assert tuple(screen.get_at((20, 94)))[:3] == (255, 255, 255)
    assert tuple(screen.get_at((20 + 20, 100)))[:3] == (10, 20, 30)
