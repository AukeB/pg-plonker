# pg-plonker

**pg-plonker** is a lightweight pygame extension for plonking GUI elements down on your pygame window. It follows pygame's own conventions closely, so if you already know pygame, you already know most of pg-plonker.

---

## Installation

pg-plonker is not yet published to PyPI. Install it locally in editable mode from the project root:

```bash
uv sync
```

or, without uv:

```bash
pip install -e .
```

---

## Importing

The top-level package exposes the controls, the panel, the `draw` module, and the config models. The convention is to import it as `pgp`:

```python
import pg_plonker as pgp

button = pgp.Button(surface=screen, x=100, y=100)
panel = pgp.GUIPanel(surface=screen)
pgp.draw.button(surface=screen, x=100, y=200, width=180, height=36, text="Toggle grid")
```

Each name is also available from its module, such as `from pg_plonker.gui_panel import GUIPanel`.

---

## Quick start

```python
import pygame as pg

from pg_plonker.gui_panel import GUIPanel
from pg_plonker.utils import get_window_size_from_screen_resolution

pg.init()
window_size = get_window_size_from_screen_resolution()
screen = pg.display.set_mode(window_size)

panel = GUIPanel(surface=screen)
show_grid = panel.add_button(text="Show grid")
show_vectors = panel.add_button(text="Show vectors")

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        panel.handle_event(event)

    screen.fill((255, 255, 255))

    if show_grid.value:
        draw_grid()

    if show_vectors.value:
        draw_vectors()

    panel.draw()
    pg.display.flip()

pg.quit()
```

---

## Drawing functions

pg-plonker exposes a `draw` module that mirrors `pygame.draw` — stateless functions that take a surface and draw onto it. These are the lowest-level building blocks.

### `draw.button`

```python
from pg_plonker import draw

draw.button(
    surface=screen,
    x=100,
    y=100,
    width=180,
    height=36,
    text="Toggle grid",
)
```

All visual parameters are optional and fall back to the active style, but can be overridden per call:

```python
draw.button(
    surface=screen,
    x=100,
    y=100,
    width=180,
    height=36,
    text="Toggle grid",
    font_name="arial",
    font_size=24,
    color_background=(200, 100, 100),
    color_border=(0, 0, 0),
    color_text=(255, 255, 255),
    color_text_shadow=(0, 0, 0),
    border_width=3,
    border_width_inner=2,
    text_shadow_offset=2,
)
```

`draw.button` is intentionally stateless — it draws and forgets. Use it when you want full manual control over position and appearance, or when building your own controls on top of pg-plonker.

---

## Controls

Controls are stateful wrappers around the draw functions. They remember their state, handle events, and redraw themselves correctly.

### `Button`

A `Button` can be created directly:

```python
from pg_plonker.controls.button import Button

show_grid = Button(surface=screen, x=100, y=100, text="Show grid")
```

or via a `GUIPanel`, which handles positioning automatically (see below).

A `Button` is the value — read its state directly:

```python
if show_grid.value:
    draw_grid()
```

Forward events to it in your event loop:

```python
for event in pg.event.get():
    show_grid.handle_event(event)
```

`Button.handle_event` mutates `value` in place and returns `None` — polling `.value` each frame is the intended pattern.

---

## `GUIPanel`

`GUIPanel` is a vertical side panel that owns and lays out controls for you — no manual coordinate work required.

```python
from pg_plonker.gui_panel import GUIPanel

panel = GUIPanel(surface=screen)

show_grid = panel.add_button(text="Show grid")
show_vectors = panel.add_button(text="Show vectors")
show_noise = panel.add_button(text="Show noise")
```

Each `add_button` call stacks the new button vertically below the previous one.

In your event loop, forward events to the panel — it takes care of translating coordinates and dispatching to all registered controls:

```python
for event in pg.event.get():
    panel.handle_event(event)
```

And draw it each frame, after clearing the screen and before flipping the display:

```python
panel.draw()
```

Panel appearance comes from the active style, and the layout options are plain arguments that can be set per instance:

```python
panel = GUIPanel(surface=screen, width=300, color_background=(20, 20, 20))
```

---

## Styles

The look of every control comes from the active style. The default style is `embossed`.

Available styles:

- `"embossed"` (default): raised 3D controls with light and dark bevels.
- `"flat"`: no borders or bevels, and no hover or press effects.
- `"soft"`: light pastel colours, subtle text shadows and gentle hover.
- `"terminal"`: monospace text, green on black, with green borders.
- `"chalk"`: dark slate panel with sand-coloured buttons, a gold on state with dark text, and rounded corners.

Every control and draw function reads the active style, so a call to `set_style()` changes all of them:

```python
import pg_plonker as pgp

pgp.set_style("embossed")
```

Each style sets every value in the `Style` dataclass and its element groups, so a style is always complete. Passing a value to a constructor, such as `Button(..., color_text=(0, 0, 0))`, overrides the style for that control, for as long as the control exists. Calling `set_style()` does not change it. Arguments left out follow the active style, so they change when the style does.

Layout options such as the panel's `width`, `margin_gui_panel`, `margin_button` and `align_right` are plain arguments of `GUIPanel`, not part of a style.

---

## Future additions

pg-plonker is under active development. A prioritized list of what's planned but not yet built lives in [`TODO.md`](TODO.md):

- Button press animations and click sound effects
- More styles (`flat`, `chalk`, `terminal`, `soft`)
- PyPI publishing