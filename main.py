"""Module for testing the pygame_ui Button class."""

import pygame as pg

from src.pg_plonker.controls.button import Button
from src.pg_plonker.gui_config_models import UIConfig
from src.pg_plonker.utils import get_window_size_from_screen_resolution


def main() -> None:
    config = UIConfig()

    pg.init()
    window_size = get_window_size_from_screen_resolution()
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("pygame_ui test")

    window_width, window_height = window_size
    
    button_rect = pg.Rect(
        (window_width - config.button.width) // 2,
        (window_height - config.button.height) // 2,
        config.button.width,
        config.button.height,
    )

    toggle_button = Button(
        surface=screen,
        rect=button_rect,
        text="Toggle grid",
        state=False,
    )

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False

            toggle_button.handle_event(event)

        screen.fill(config.panel.color_background)
        toggle_button.draw()
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()