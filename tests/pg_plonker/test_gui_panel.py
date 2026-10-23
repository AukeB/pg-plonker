"""Tests for the gui_panel module."""

import pygame as pg

from pg_plonker.controls import Button, Dropdown
from pg_plonker.gui_panel import GUIPanel


def _mouse_down(pos: tuple[int, int]) -> pg.event.Event:
    """Create a primary mouse button press event.

    Args:
        pos (tuple[int, int]): Position of the press in screen coordinates.

    Returns:
        event (pg.event.Event): The press event.
    """

    event = pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=pos)

    return event


def _mouse_up(pos: tuple[int, int]) -> pg.event.Event:
    """Create a primary mouse button release event.

    Args:
        pos (tuple[int, int]): Position of the release in screen coordinates.

    Returns:
        event (pg.event.Event): The release event.
    """

    event = pg.event.Event(pg.MOUSEBUTTONUP, button=1, pos=pos)

    return event


def _mouse_motion(pos: tuple[int, int]) -> pg.event.Event:
    """Create a mouse motion event.

    Args:
        pos (tuple[int, int]): Position the mouse moved to, in screen
            coordinates.

    Returns:
        event (pg.event.Event): The motion event.
    """

    event = pg.event.Event(pg.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0))

    return event


# Testing the "__init__" method from the "GUIPanel" class.


def test_init_anchors_panel_to_the_right(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    assert panel.rect_panel == pg.Rect(800 - 620, 0, 620, 600)
    assert panel.divider_x == 800 - 620


def test_init_can_anchor_panel_to_the_left(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen, align_right=False)

    assert panel.rect_panel.x == 0
    assert panel.divider_x == 620


# Testing the "add_button" method from the "GUIPanel" class.


def test_add_button_centers_and_stacks_controls(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    first = panel.add_button(text="Grid")
    second = panel.add_button(text="Gradients")

    assert isinstance(first, Button)
    assert first.rect == pg.Rect((620 - 540) // 2, 40, 540, 108)
    assert second.rect.y == 40 + 108 + 24


# Testing the "add_slider" method from the "GUIPanel" class.


def test_add_slider_reserves_vertical_margins(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    slider = panel.add_slider(start=0, stop=10, value=5)

    assert slider.y == 40 + slider.margin_vertical + slider.rect.height // 2
    assert panel._next_control_y == 40 + slider.margin_vertical * 2 + slider.rect.height + 24


# Testing the "add_dropdown" method from the "GUIPanel" class.


def test_add_dropdown_places_header_and_advances_cursor(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    dropdown = panel.add_dropdown(options=["Easy", "Hard"])

    assert isinstance(dropdown, Dropdown)
    assert dropdown.rect.y == 40
    assert panel._next_control_y == 40 + 72 + 24


# Testing the "_translate_event_to_local" method from the "GUIPanel" class.


def test_translate_passes_through_events_without_position(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    key_event = pg.event.Event(pg.KEYDOWN, key=pg.K_a)

    translated = panel._translate_event_to_local(key_event)

    assert translated is key_event


def test_translate_shifts_positions_outside_the_panel_too(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    event = _mouse_down((10, 10))
    translated = panel._translate_event_to_local(event)

    assert translated.pos == (10 - (800 - 620), 10)


def test_translate_shifts_position_into_panel_coordinates(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)

    event = _mouse_down((800 - 620 + 50, 70))
    translated = panel._translate_event_to_local(event)

    assert translated is not None
    assert translated.pos == (50, 70)


# Testing the "handle_event" method from the "GUIPanel" class.


def test_handle_event_forwards_clicks_to_controls(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    button = panel.add_button(text="Grid")
    click_x = 800 - 620 + 40 + 270
    click_y = 40 + 54

    event = _mouse_down((click_x, click_y))
    panel.handle_event(event)
    event = _mouse_up((click_x, click_y))
    panel.handle_event(event)

    assert button.value is True


def test_handle_event_ignores_clicks_outside_the_panel(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    button = panel.add_button(text="Grid")

    event = _mouse_down((10, 10))
    panel.handle_event(event)
    event = _mouse_up((10, 10))
    panel.handle_event(event)

    assert button.value is False


def test_handle_event_forwards_non_mouse_events(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    panel.add_button(text="Grid")

    event = pg.event.Event(pg.KEYDOWN, key=pg.K_a)
    panel.handle_event(event)


def test_outside_click_closes_an_open_dropdown(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    dropdown = panel.add_dropdown(options=["Easy", "Hard"])
    dropdown.is_open = True

    event = _mouse_down((10, 10))
    panel.handle_event(event)

    assert dropdown.is_open is False


def test_outside_non_click_leaves_open_dropdown_open(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    dropdown = panel.add_dropdown(options=["Easy", "Hard"])
    dropdown.is_open = True

    event = pg.event.Event(pg.MOUSEMOTION, pos=(10, 10), rel=(0, 0), buttons=(0, 0, 0))
    panel.handle_event(event)

    assert dropdown.is_open is True


def test_open_dropdown_takes_exclusive_events(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    button = panel.add_button(text="Grid")
    dropdown = panel.add_dropdown(options=["Easy", "Hard"])
    dropdown.is_open = True
    button_click = (800 - 620 + 40 + 270, 40 + 54)

    event = _mouse_down(button_click)
    panel.handle_event(event)
    event = _mouse_up(button_click)
    panel.handle_event(event)

    assert button.value is False


def test_release_outside_the_panel_ends_a_button_press(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    button = panel.add_button(text="Grid")
    button_center = (800 - 620 + 40 + 270, 40 + 54)

    panel.handle_event(_mouse_down(button_center))
    panel.handle_event(_mouse_motion((10, 10)))
    panel.handle_event(_mouse_up((10, 10)))
    panel.handle_event(_mouse_motion(button_center))
    button.draw()
    light_bevel = screen.get_at((800 - 620 + 40 + 100, 40 + 6))

    assert button.value is False
    assert tuple(light_bevel)[:3] == (198, 198, 198)


def test_release_outside_the_panel_ends_a_slider_drag(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    slider = panel.add_slider(start=0, stop=10)
    panel_x = 800 - 620
    handle_x, handle_y = slider._get_handle_center()

    panel.handle_event(_mouse_down((panel_x + handle_x, handle_y)))
    panel.handle_event(_mouse_up((10, 10)))
    panel.handle_event(_mouse_motion((panel_x + slider.x + slider.width, slider.y)))

    assert slider.value == 0


def test_release_outside_the_panel_ends_a_dropdown_header_press(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    dropdown = panel.add_dropdown(options=["Easy", "Hard"])
    panel_x = 800 - 620
    header_center = (panel_x + dropdown.rect.centerx, dropdown.rect.centery)

    panel.handle_event(_mouse_down(header_center))
    panel.handle_event(_mouse_up((10, 10)))
    panel.handle_event(_mouse_up(header_center))

    assert dropdown.is_open is False


# Testing the "draw" method from the "GUIPanel" class.


def test_draw_renders_controls_and_divider(screen: pg.Surface) -> None:
    panel = GUIPanel(surface=screen)
    panel.add_button(text="Grid")
    dropdown = panel.add_dropdown(options=["Easy", "Hard"])
    dropdown.is_open = True

    panel.draw()

    assert pg.transform.average_color(screen)[:3] != (0, 0, 0)
