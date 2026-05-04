"""Module for testing the pygame_ui Button class."""

import pygame as pg

from src.pg_plonker.gui_panel import GUIPanel
from src.pg_plonker.utils import get_window_size_from_screen_resolution


def main() -> None:
    pg.init()
    window_size = get_window_size_from_screen_resolution()
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("pygame_ui test")
    
    gui_panel = GUIPanel(surface=screen, right_side=False)

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