"""Module for testing the pygame_ui Button class."""

import pygame as pg

from src.pg_plonker.gui_panel import GUIPanel
from src.pg_plonker.controls.button import Button
from src.pg_plonker.utils import get_window_size_from_screen_resolution


def main() -> None:
    pg.init()
    window_size = get_window_size_from_screen_resolution()
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("PyGame Plonker")
    
    gui_panel = GUIPanel(surface=screen)

    button = Button(
        surface=screen,
        rect=pg.Rect(0, 0, 800, 200),
        text="Press me"
    )

    gui_panel.add(button=button)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False

        screen.fill((255, 255, 255))
        gui_panel.draw()
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()