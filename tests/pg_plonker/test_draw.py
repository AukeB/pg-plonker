"""Tests for the draw module."""

import pygame as pg

from pg_plonker import draw

# Testing the "button" function.


def test_button_fills_background_with_given_color(screen: pg.Surface, font: pg.font.Font) -> None:
    draw.button(surface=screen,
        font=font, x=20, y=20, color_background=(10, 20, 30))

    pixel = screen.get_at((20 + 540 - 30, 20 + 54))

    assert tuple(pixel)[:3] == (10, 20, 30)


def test_button_uses_config_defaults_when_no_overrides(screen: pg.Surface, font: pg.font.Font) -> None:
    draw.button(surface=screen,
        font=font, x=20, y=20)

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


def test_button_pressed_does_not_move_the_button(screen: pg.Surface, font: pg.font.Font) -> None:
    screen.fill((255, 255, 255))

    draw.button(
        surface=screen,
        font=font,
        x=20,
        y=20,
        color_background=(10, 20, 30),
        pressed=True,
    )

    top_left_corner = screen.get_at((20 + 1, 20 + 1))
    background_middle = screen.get_at((20 + 100, 20 + 20))

    assert tuple(top_left_corner)[:3] == (0, 0, 0)
    assert tuple(background_middle)[:3] == (10, 20, 30)


def test_button_pressed_swaps_bevel_colors(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_slider_draws_the_filled_part_up_to_the_handle(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_slider_shows_value_when_requested(screen: pg.Surface, font: pg.font.Font) -> None:
    draw.slider(surface=screen,
        font=font, x=20, y=100, start=0, stop=10, value=3.5, precision=2, show_value=True)

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


# Testing the "dropdown_header" function.


def test_dropdown_header_draws_closed_and_open_states(screen: pg.Surface, font: pg.font.Font) -> None:
    draw.dropdown_header(surface=screen,
        font=font, x=20, y=20, text="Easy", is_open=False)

    closed_average = pg.transform.average_color(screen)[:3]

    screen.fill((0, 0, 0))

    draw.dropdown_header(surface=screen,
        font=font, x=20, y=20, text="Easy", is_open=True)

    open_average = pg.transform.average_color(screen)[:3]

    assert closed_average != (0, 0, 0)
    assert open_average != (0, 0, 0)


# Testing the "dropdown_options" function.


def test_dropdown_options_paints_the_hovered_row(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_dropdown_options_without_hover_uses_default_color(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_dropdown_options_separator_is_border_width_thick(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_dropdown_options_outer_border_is_border_width_thick(screen: pg.Surface, font: pg.font.Font) -> None:
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


def test_dropdown_options_top_border_overlaps_header_bottom_border(screen: pg.Surface, font: pg.font.Font) -> None:
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
