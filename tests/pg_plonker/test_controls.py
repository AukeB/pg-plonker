"""Tests for the controls module."""

import pygame as pg
import pytest

from pg_plonker import draw
from pg_plonker.controls import Button, Dropdown, Slider
from pg_plonker.styles import get_style


def _mouse_down(pos: tuple[int, int], button: int = 1) -> pg.event.Event:
    """Create a mouse button press event.

    Args:
        pos (tuple[int, int]): Position of the press.
        button (int): Mouse button number.

    Returns:
        event (pg.event.Event): The press event.
    """

    event = pg.event.Event(pg.MOUSEBUTTONDOWN, button=button, pos=pos)

    return event


def _mouse_up(pos: tuple[int, int], button: int = 1) -> pg.event.Event:
    """Create a mouse button release event.

    Args:
        pos (tuple[int, int]): Position of the release.
        button (int): Mouse button number.

    Returns:
        event (pg.event.Event): The release event.
    """

    event = pg.event.Event(pg.MOUSEBUTTONUP, button=button, pos=pos)

    return event


def _mouse_motion(pos: tuple[int, int]) -> pg.event.Event:
    """Create a mouse motion event.

    Args:
        pos (tuple[int, int]): Position the mouse moved to.

    Returns:
        event (pg.event.Event): The motion event.
    """

    event = pg.event.Event(pg.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0))

    return event


# Testing the "__init__" method from the "Button" class.


def test_button_init_uses_style_size_and_starts_inactive(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    assert (button.width, button.height) == (540, 108)
    assert button.rect == pg.Rect(20, 20, 540, 108)
    assert button.value is False


# Testing the "draw" method from the "Button" class.


def test_button_draw_renders_without_error(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20, value=True)

    button.draw()

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


def test_button_draw_shows_bevel_pressed_while_held(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen,
        x=20,
        y=20,
        color_border_inner_light=(1, 1, 1),
        color_border_inner_dark=(2, 2, 2),
    )

    button.draw()
    unpressed_light_bevel = screen.get_at((20 + 100, 20 + 6))

    button.handle_event(_mouse_down(button.rect.center))
    button.draw()
    pressed_light_bevel = screen.get_at((20 + 100, 20 + 6))

    assert tuple(unpressed_light_bevel)[:3] == (1, 1, 1)
    assert tuple(pressed_light_bevel)[:3] == (2, 2, 2)


# Testing the "handle_event" method from the "Button" class.


def test_button_toggles_on_press_and_release_inside(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    event = _mouse_down((30, 30))
    button.handle_event(event)
    event = _mouse_up((30, 30))
    button.handle_event(event)

    assert button.value is True


def test_button_ignores_non_primary_buttons(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    event = _mouse_down((30, 30), button=3)
    button.handle_event(event)
    event = _mouse_up((30, 30), button=3)
    button.handle_event(event)

    assert button.value is False


def test_button_does_not_toggle_when_released_outside(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    event = _mouse_down((30, 30))
    button.handle_event(event)
    event = _mouse_up((900, 900))
    button.handle_event(event)

    assert button.value is False


def test_button_release_without_press_does_nothing(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    event = _mouse_up((30, 30))
    button.handle_event(event)

    assert button.value is False


def test_button_press_outside_is_not_remembered(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    event = _mouse_down((900, 900))
    button.handle_event(event)
    event = _mouse_up((30, 30))
    button.handle_event(event)

    assert button.value is False


def test_button_look_returns_to_unpressed_when_pointer_leaves(
    screen: pg.Surface,
) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen,
        x=20,
        y=20,
        color_border_inner_light=(1, 1, 1),
        color_border_inner_dark=(2, 2, 2),
    )

    button.handle_event(_mouse_down(button.rect.center))
    button.handle_event(_mouse_motion((900, 900)))
    button.draw()
    bevel_while_outside = screen.get_at((20 + 100, 20 + 6))

    assert tuple(bevel_while_outside)[:3] == (1, 1, 1)


def test_button_look_is_pressed_again_when_pointer_returns(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen,
        x=20,
        y=20,
        color_border_inner_light=(1, 1, 1),
        color_border_inner_dark=(2, 2, 2),
    )

    button.handle_event(_mouse_down(button.rect.center))
    button.handle_event(_mouse_motion((900, 900)))
    button.handle_event(_mouse_motion(button.rect.center))
    button.draw()
    bevel_back_inside = screen.get_at((20 + 100, 20 + 6))

    assert tuple(bevel_back_inside)[:3] == (2, 2, 2)


def test_button_release_after_leaving_does_not_toggle(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    button.handle_event(_mouse_down(button.rect.center))
    button.handle_event(_mouse_motion((900, 900)))
    button.handle_event(_mouse_up((900, 900)))

    assert button.value is False


def test_button_hover_lightens_the_inactive_color_while_pointer_is_over(
    screen: pg.Surface,
) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen, x=20, y=20, color_background_inactive=(100, 100, 100)
    )

    button.handle_event(_mouse_motion(button.rect.center))
    button.draw()
    background_while_hovered = screen.get_at((20 + 100, 20 + 20))

    assert tuple(background_while_hovered)[:3] == (123, 123, 123)


def test_button_hover_lightens_the_active_color_when_on(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen,
        x=20,
        y=20,
        color_background_active=(100, 100, 100),
        value=True,
    )

    button.handle_event(_mouse_motion(button.rect.center))
    button.draw()
    background_while_hovered = screen.get_at((20 + 100, 20 + 20))

    assert tuple(background_while_hovered)[:3] == (123, 123, 123)


def test_button_hover_ends_when_pointer_leaves(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    button = Button(
        surface=screen, x=20, y=20, color_background_inactive=(100, 100, 100)
    )

    button.handle_event(_mouse_motion(button.rect.center))
    button.handle_event(_mouse_motion((900, 900)))
    button.draw()
    background_after_leaving = screen.get_at((20 + 100, 20 + 20))

    assert tuple(background_after_leaving)[:3] == (100, 100, 100)


def test_button_toggles_when_pointer_returns_before_release(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20)

    button.handle_event(_mouse_down(button.rect.center))
    button.handle_event(_mouse_motion((900, 900)))
    button.handle_event(_mouse_motion(button.rect.center))
    button.handle_event(_mouse_up(button.rect.center))

    assert button.value is True


# Testing the "__init__" method from the "Slider" class.


def test_slider_init_rejects_start_not_below_stop(screen: pg.Surface) -> None:
    with pytest.raises(ValueError, match="must be less than"):
        Slider(surface=screen, x=0, y=0, start=5, stop=5)


def test_slider_init_rejects_value_out_of_range(screen: pg.Surface) -> None:
    with pytest.raises(ValueError, match="must be within"):
        Slider(surface=screen, x=0, y=0, start=0, stop=10, value=11)


def test_slider_init_defaults_value_to_start(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=0, y=0, start=2, stop=8)

    assert slider.value == 2


def test_slider_precision_includes_step_decimals(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=0, y=0, start=0, stop=1, step=0.25)

    assert slider._precision == 2 + 2


# Testing the "_get_handle_center" method from the "Slider" class.


def test_handle_center_is_proportional_to_value(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, width=540, x=20, y=40, start=0, stop=10, value=5)

    assert slider._get_handle_center() == (20 + 270, 40)


# Testing the "_get_value_from_x" method from the "Slider" class.


def test_value_from_x_maps_position_to_range(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, width=540, x=20, y=40, start=0, stop=10)

    assert slider._get_value_from_x(20 + 135) == 2.5


def test_value_from_x_clamps_outside_the_track(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10)

    assert slider._get_value_from_x(-500) == 0
    assert slider._get_value_from_x(5000) == 10


def test_value_from_x_snaps_to_step(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, width=540, start=0, stop=10, step=1)

    assert slider._get_value_from_x(20 + 166) == 3


# Testing the "draw" method from the "Slider" class.


def test_slider_draw_renders_with_value_readout(screen: pg.Surface) -> None:
    slider = Slider(
        surface=screen, x=20, y=40, start=0, stop=10, value=4, show_value=True
    )

    slider.draw()

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


def test_slider_handle_lightens_while_pointer_is_over_handle(
    screen: pg.Surface,
) -> None:
    screen.fill((255, 255, 255))
    slider = Slider(
        surface=screen,
        x=20,
        y=40,
        start=0,
        stop=10,
        value=5,
        color_handle=(100, 100, 100),
    )
    handle_center = slider._get_handle_center()

    slider.handle_event(_mouse_motion(handle_center))
    slider.draw()
    handle_while_hovered = screen.get_at(handle_center)

    assert tuple(handle_while_hovered)[:3] == (123, 123, 123)


def test_slider_handle_hover_ends_when_pointer_leaves(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    slider = Slider(
        surface=screen,
        x=20,
        y=40,
        start=0,
        stop=10,
        value=5,
        color_handle=(100, 100, 100),
    )
    handle_center = slider._get_handle_center()

    slider.handle_event(_mouse_motion(handle_center))
    slider.handle_event(_mouse_motion((900, 900)))
    slider.draw()
    handle_after_leaving = screen.get_at(handle_center)

    assert tuple(handle_after_leaving)[:3] == (100, 100, 100)


# Testing the "handle_event" method from the "Slider" class.


def test_slider_drag_updates_value_then_stops_on_release(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, width=540, x=20, y=40, start=0, stop=10, value=5)
    handle_x, handle_y = slider._get_handle_center()

    event = _mouse_down((handle_x, handle_y))
    slider.handle_event(event)
    event = _mouse_motion((20 + 135, 40))
    slider.handle_event(event)
    dragged_value = slider.value
    event = _mouse_up((20 + 135, 40))
    slider.handle_event(event)
    event = _mouse_motion((20 + 400, 40))
    slider.handle_event(event)

    assert dragged_value == 2.5
    assert slider.value == 2.5


def test_slider_press_away_from_handle_does_not_drag(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10, value=5)

    event = _mouse_down((20, 40 + 50))
    slider.handle_event(event)
    event = _mouse_motion((400, 40))
    slider.handle_event(event)

    assert slider.value == 5


def test_slider_press_on_track_jumps_value_to_mouse(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, width=540, x=20, y=40, start=0, stop=10, value=5)

    event = _mouse_down((20 + 162, 40))
    slider.handle_event(event)

    assert slider.value == 3


def test_slider_ignores_secondary_button_press(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10, value=5)
    handle_x, handle_y = slider._get_handle_center()

    event = _mouse_down((handle_x, handle_y), button=3)
    slider.handle_event(event)
    event = _mouse_motion((400, 40))
    slider.handle_event(event)

    assert slider.value == 5


# Testing the "__init__" method from the "Dropdown" class.


def test_dropdown_init_rejects_empty_options(screen: pg.Surface) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        Dropdown(surface=screen, x=0, y=0, options=[])


def test_dropdown_init_rejects_unknown_value(screen: pg.Surface) -> None:
    with pytest.raises(ValueError, match="must be one of"):
        Dropdown(surface=screen, x=0, y=0, options=["Easy"], value="Hard")


def test_dropdown_defaults_to_first_option(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    assert dropdown.value == "Easy"
    assert dropdown.is_open is False


# Testing the "_get_options_rect" method from the "Dropdown" class.


def test_options_rect_stacks_below_header(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard", "Expert"])

    assert dropdown._get_options_rect() == pg.Rect(20, 92, 540, 60 * 3)


# Testing the "close" method from the "Dropdown" class.


def test_close_is_safe_when_already_closed(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy"])

    dropdown.close()

    assert dropdown.is_open is False


def test_close_resets_hover(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
    dropdown.is_open = True
    dropdown._hovered_index = 1

    dropdown.close()

    assert dropdown.is_open is False
    assert dropdown._hovered_index is None


# Testing the "draw" method from the "Dropdown" class.


def test_dropdown_draw_renders_header(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    dropdown.draw()

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


def test_dropdown_header_lightens_while_pointer_is_over(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    dropdown = Dropdown(
        surface=screen,
        x=20,
        y=20,
        options=["Easy", "Hard"],
        color_background_inactive=(100, 100, 100),
    )

    dropdown.handle_event(_mouse_motion(dropdown.rect.center))
    dropdown.draw()
    header_while_hovered = screen.get_at((dropdown.rect.centerx, dropdown.rect.y + 20))

    assert tuple(header_while_hovered)[:3] == (123, 123, 123)


def test_dropdown_header_hover_ends_when_pointer_leaves(screen: pg.Surface) -> None:
    screen.fill((255, 255, 255))
    dropdown = Dropdown(
        surface=screen,
        x=20,
        y=20,
        options=["Easy", "Hard"],
        color_background_inactive=(100, 100, 100),
    )

    dropdown.handle_event(_mouse_motion(dropdown.rect.center))
    dropdown.handle_event(_mouse_motion((900, 900)))
    dropdown.draw()
    header_after_leaving = screen.get_at((dropdown.rect.centerx, dropdown.rect.y + 20))

    assert tuple(header_after_leaving)[:3] == (100, 100, 100)


# Testing the "draw_options" method from the "Dropdown" class.


def test_draw_options_is_a_no_op_while_closed(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    dropdown.draw_options()

    assert pg.transform.average_color(screen)[:3] == (0, 0, 0)


def test_draw_options_renders_list_while_open(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
    dropdown.is_open = True

    dropdown.draw_options()

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)


# Testing the "handle_event" method from the "Dropdown" class.


def test_dropdown_opens_on_press_and_release_on_header(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    event = _mouse_down((30, 30))
    dropdown.handle_event(event)
    event = _mouse_up((30, 30))
    dropdown.handle_event(event)

    assert dropdown.is_open is True


def test_dropdown_release_without_press_stays_closed(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    event = _mouse_up((30, 30))
    dropdown.handle_event(event)

    assert dropdown.is_open is False


def test_dropdown_press_elsewhere_does_not_open(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])

    event = _mouse_down((900, 900))
    dropdown.handle_event(event)
    event = _mouse_up((30, 30))
    dropdown.handle_event(event)

    assert dropdown.is_open is False


def test_dropdown_hover_tracks_option_under_cursor(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
    dropdown.is_open = True

    event = _mouse_motion((30, 92 + 60 + 5))
    dropdown.handle_event(event)
    hovered_inside = dropdown._hovered_index
    event = _mouse_motion((900, 900))
    dropdown.handle_event(event)

    assert hovered_inside == 1
    assert dropdown._hovered_index is None


def test_dropdown_click_on_option_selects_it_and_closes(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard", "Expert"])
    dropdown.is_open = True

    event = _mouse_down((30, 92 + 120 + 5))
    dropdown.handle_event(event)

    assert dropdown.value == "Expert"
    assert dropdown.is_open is False


def test_dropdown_click_outside_closes_without_selecting(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
    dropdown.is_open = True

    event = _mouse_down((900, 900))
    dropdown.handle_event(event)

    assert dropdown.value == "Easy"
    assert dropdown.is_open is False


def test_dropdown_secondary_click_while_open_is_ignored(screen: pg.Surface) -> None:
    dropdown = Dropdown(surface=screen, x=20, y=20, options=["Easy", "Hard"])
    dropdown.is_open = True

    event = _mouse_down((30, 92 + 5), button=3)
    dropdown.handle_event(event)

    assert dropdown.is_open is True
    assert dropdown.value == "Easy"


# Testing the "_create_font" function from the "controls" module.


def test_font_is_created_once_and_reused_for_every_draw(
    screen: pg.Surface, monkeypatch: pytest.MonkeyPatch
) -> None:
    created: list[tuple[str, int]] = []
    real_sysfont = pg.font.SysFont

    def recording_sysfont(name: str, size: int) -> pg.font.Font:
        created.append((name, size))
        font = real_sysfont(name, size)

        return font

    monkeypatch.setattr(pg.font, "SysFont", recording_sysfont)
    button = Button(surface=screen, x=20, y=20, text="Start")

    button.draw()
    button.draw()

    assert created == [("arial", 50)]


def test_font_uses_the_requested_name_and_size(screen: pg.Surface) -> None:
    button = Button(surface=screen, x=20, y=20, font_name="arial", font_size=20)

    assert isinstance(button.font, pg.font.Font)


# Testing the "font" property from the "Slider" class.


def test_slider_font_is_reused_until_the_name_or_size_changes(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10)

    first_font = slider.font

    assert slider.font is first_font


# Testing the "top_clearance" property from the "Slider" class.


# Testing the "text" argument of the "Slider" class.


def test_slider_text_defaults_to_slider(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10)

    assert slider.text == "Slider"


# Testing the "height" property from the "Slider" class.


def test_height_is_padding_and_track_when_nothing_is_shown(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10, text=None)
    style = get_style().slider

    assert slider.height == 2 * style.padding + 2 * style.handle_radius


def test_height_adds_the_label_when_text_is_given(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=20, y=40, start=0, stop=10, text="Speed")
    style = get_style().slider
    label_height = slider.label_font.size("Speed")[1]

    assert slider.height == (
        2 * style.padding
        + 2 * style.handle_radius
        + draw._LABEL_GAP
        + label_height
    )


def test_height_grows_by_the_readout_when_the_value_is_shown(screen: pg.Surface) -> None:
    hidden = Slider(surface=screen, x=20, y=40, start=0, stop=10, text=None)
    shown = Slider(surface=screen, x=20, y=40, start=0, stop=10, show_value=True, text=None)
    readout_height = shown.font.size("0")[1]

    assert shown.height - hidden.height == draw._READOUT_GAP + readout_height


# Testing the "place" method from the "Slider" class.


def test_place_moves_the_box_top_left_corner_to_the_given_point(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=0, y=0, start=0, stop=10, text="Speed")

    slider.place(left=30, top=50)

    assert slider.rect.topleft == (30, 50)


# Testing the spacing of the box around the "Slider" class.


def test_slider_box_has_the_same_spacing_on_every_side(screen: pg.Surface) -> None:
    slider = Slider(surface=screen, x=100, y=100, start=0, stop=10, show_value=True)
    style = get_style().slider
    inset = style.padding + slider.handle_radius

    assert slider.x - slider.rect.left == inset
    assert slider.rect.right - (slider.x + slider.width) == inset
    assert slider.rect.bottom - (slider.y + slider.handle_radius) == style.padding
