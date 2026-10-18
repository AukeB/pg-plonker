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
