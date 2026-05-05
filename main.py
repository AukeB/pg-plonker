"""Module for testing the pg_plonker GUIPanel class."""

import pygame as pg

from src.pg_plonker.controls.button import Button
from src.pg_plonker.gui_panel import GUIPanel
from src.pg_plonker.utils import get_window_size_from_screen_resolution


def main() -> None:
    pg.init()
    window_size = get_window_size_from_screen_resolution()
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("PyGame Plonker - GUIPanel Test")

    panel = GUIPanel(surface=screen)

    for index in range(5):
        panel.add_button(text=f"Button {index + 1}")

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False

            panel.handle_event(event)

        screen.fill((255, 255, 255))
        panel.draw()

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()



"""
TODO:

BUGS/CODE IMPROVEMENTS
- All the 'or' statements have a weakness. For example if equal to 0, False, or "" empty strings.

FEATURES
- Button click animations so that you can actually see the button being pressed
- Sound animations when button clicking
"""