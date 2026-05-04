# pg-plonker

**pg-plonker** is a lightweight pygame extension for plonking GUI elements down on your pygame window. It follows pygame's own conventions closely, so if you already know pygame, you already know most of pg-plonker.

> Developed using an API-first design approach — the public interface was designed before a single line of implementation was written.

---

## Installation

```bash
pip install pg-plonker
```

---

## Quick start

```python
import pygame as pg
import pgplonker as pgp

pg.init()
screen = pg.display.set_mode((1280, 720))

pgp.set_style("embossed")
pgp.set_mode("gui_panel", surface=screen)

show_grid = pgp.Button("Show grid")
show_vectors = pgp.Button("Show vectors")

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if show_grid.state:
        draw_grid()

    if show_vectors.state:
        draw_vectors()

    pg.display.flip()

pg.quit()
```

---

## Drawing functions

pg-plonker exposes a `draw` module that mirrors `pygame.draw` — stateless functions that take a surface and draw onto it. These are the lowest-level building blocks.

### `pgp.draw.button`

```python
pgp.draw.button(
    surface=screen,
    rect=pg.Rect(100, 100, 180, 36),
    text="Toggle grid",
    font=my_font,
)
```

All visual parameters have sensible defaults and can be overridden per call:

```python
pgp.draw.button(
    surface=screen,
    rect=pg.Rect(100, 100, 180, 36),
    text="Toggle grid",
    font=my_font,
    background_color=(200, 100, 100),
    border_color=(0, 0, 0),
    text_color=(255, 255, 255),
    text_shadow_color=(0, 0, 0),
    border_width=3,
    text_shadow_offset=2,
    border_width_inner=2,
)
```

`pgp.draw.button` is intentionally stateless — it draws and forgets. Use it when you want full manual control over position and appearance, or when building your own controls on top of pg-plonker.

---

## Controls

Controls are stateful wrappers around the draw functions. They remember their state, handle events, and redraw themselves correctly.

### `pgp.Button`

```python
show_grid = pgp.Button("Show grid")
```

A `Button` is the value. Read its state directly:

```python
if show_grid.state:
    draw_grid()
```

Handle events by passing them to the button:

```python
for event in pg.event.get():
    show_grid.handle_event(event)
```

---

## Styles

pg-plonker ships with a set of pre-made visual styles. A style defines all visual properties for every control — colors, sizes, fonts, border behaviour — so you only have to set one thing.

```python
pgp.set_style("embossed")   # raised 3D buttons with light/dark inner borders creating depth
pgp.set_style("flat")       # clean, minimal, no borders or shadows
pgp.set_style("chalk")      # dark background with soft, muted tones and rounded feel
pgp.set_style("terminal")   # monospace font, green on black, inspired by CLI interfaces
pgp.set_style("soft")       # light pastel colors, subtle shadows, friendly and modern
```

Call `set_style` before creating any controls. All subsequently created controls will use that style's defaults.

You can still override individual properties per control even after setting a style:

```python
pgp.set_style("embossed")

# All defaults come from embossed, but this button has a custom background
special_button = pgp.Button("Special", config=pgp.ButtonConfig(color_background_inactive=(180, 60, 60)))
```

Each style defines exactly the properties that style needs. For example, `"embossed"` defines `border_width_inner`, `color_border_inner_light`, and `color_border_inner_dark` — properties that simply do not exist in `"flat"` because that style has no inner borders. Your IDE will suggest only the valid properties for whichever style is active.

---

## Modes

Modes change how pg-plonker manages layout. Without a mode, you position everything manually using `pgp.draw.*`. With a mode, pg-plonker takes over layout automatically.

### `"gui_panel"`

Attaches a side panel to the pygame window. Controls registered after calling `set_mode("gui_panel")` are automatically stacked vertically in the panel — no coordinate work required.

```python
pgp.set_mode("gui_panel", surface=screen)

# These buttons are automatically positioned in the panel, top to bottom.
show_grid = pgp.Button("Show grid")
show_vectors = pgp.Button("Show vectors")
show_noise = pgp.Button("Show noise")
```

Panel appearance is controlled by `PanelConfig`, which like everything else has sensible defaults and can be overridden:

```python
pgp.set_mode(
    "gui_panel",
    surface=screen,
    config=pgp.PanelConfig(width=300, color_background=(20, 20, 20)),
)
```

---

## Design philosophy

**Familiar by design.** pg-plonker follows pygame's own conventions. `pgp.draw.button` works like `pg.draw.rect`. `pgp.set_mode` works like `pg.display.set_mode`. If you know pygame, the learning curve is nearly flat.

**Defaults for everything, except what should always be explicit.** You should never have to specify a color, font, or border width just to put a button on screen. The only required argument to `pgp.Button` is the label text, because that is the one thing pg-plonker cannot guess for you.

**Everything is overridable.** Defaults are a starting point, not a constraint. Every visual property can be overridden at the style level, the control level, or the individual draw-call level.

**Styles are complete, not cosmetic.** A style is not just a color palette — it defines the visual structure of each control. The `"embossed"` style renders inner borders that create a sense of depth; the `"flat"` style does not have inner borders at all. Each style ships with exactly the config fields it needs.

**API-first.** The public interface was designed before any implementation. The question asked first was: what should working with this feel like? The answer drove every subsequent decision.