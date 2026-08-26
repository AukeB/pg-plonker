"""Module for running the pg-plonker demo application."""

import pygame as pg

from pg_plonker.gui_panel import GUIPanel
from pg_plonker.controls import Button, Slider
from pg_plonker.utils import get_window_size_from_screen_resolution


def main() -> None:
    """
    Run the pg-plonker demo application.

    Initializes pygame, opens a window sized relative to the desktop
    resolution, and attaches a GUIPanel populated with a handful of test
    buttons. The event loop runs until the window is closed or Escape is
    pressed.

    1. Initialize pygame and open the display window.
    2. Attach a GUIPanel to the window and populate it with test buttons.
    3. Run the event loop, forwarding events to the panel each frame.
    4. Clear the screen, draw the panel, and flip the display each frame.
    5. Quit pygame once the loop exits.
    """
    pg.init()
    window_size = get_window_size_from_screen_resolution()
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("PyGame Plonker Testing")

    panel = GUIPanel(surface=screen)

    button = panel.add_button()
    slider = panel.add_slider(start=0, stop=10)

    #button = Button(surface=screen, x=100, y=100)
    #slider = Slider(surface=screen, x=100, y=300, start=0, stop=10, show_value=True)

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False

            panel.handle_event(event)
            #button.handle_event(event)
            #slider.handle_event(event)

        screen.fill((255, 255, 255))
        panel.draw()
        #button.draw()
        #slider.draw()

        print(f"{button.value}")
        print(f"{slider.value}")

        

        #print(slider.value)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()