# TODO

Planned work for pg-plonker, sorted by priority (highest first). See `README.md` for a description of what currently exists.

---

## Done

### Controls (`Button`)

- [x] Stateless `draw.button` function for manual drawing.
- [x] Stateful `Button` control with active/inactive toggle state.
- [x] `Button.handle_event` press/release handling, mutating `value` in place.
- [x] Full styling surface on `Button`/`draw.button`: size, font, borders (outer + inner light/dark), background per state, text color, and text shadow — all independently overridable.

### Layout & panel (`GUIPanel`)

- [x] `GUIPanel` container with automatic vertical layout via `add_button`.
- [x] `GUIPanel.handle_event`: coordinate translation and event forwarding to all registered controls.
- [x] `GUIPanel.draw`: panel background, divider, and all child controls.
- [x] Panel alignment support (left/right anchoring via `align_right`).

### Configuration

- [x] `ButtonConfig` and `GUIPanelConfig` default config models (since replaced by the `Style` dataclass in section 3).
- [x] Removed unused `PGPlonkerConfig` aggregate.

### Utilities

- [x] Fonts are created per control and reused until the font name or size changes, so `pg.font.SysFont` is not called on every draw.
- [x] `get_window_size_from_screen_resolution` utility for sizing the window relative to the desktop.
- [x] `WINDOW_SIZE_SCREEN_FRACTION` project constant for that sizing ratio.

### Code quality

- [x] Consistent `None`-based default fallback everywhere (`x if x is not None else default`), fixing the earlier `x or default` bug where falsy overrides (`0`, `False`) were silently ignored.
- [x] `Button.handle_event` and `GUIPanel.handle_event` both return `None`, consistent with the "poll `.value` yourself" usage pattern.

---

## 1. New GUI elements

- [x] Design `Slider` control API (value range, step, drag handling).
- [x] Implement `draw.slider` stateless drawing function.
- [x] Implement `Slider` class (value, `handle_event`, `draw`).
- [x] Add a `SliderConfig` default config model.
- [x] Wire `Slider` into `GUIPanel.add_slider` for automatic layout.
- [x] Add a `text` label to `Slider` (default `"Slider"`), drawn above the track, aligned with the handle's left edge, in a larger font than the value.
- [x] Draw the slider inside a bevelled box that matches the button, holding the label, the value (when shown) and the track. The box is taller when the value is shown, and the panel moves the next control down by its height.
- [x] Design `Dropdown` control API (options list, selected value, open/closed state).
- [x] Implement `draw.dropdown` stateless drawing function (as `draw.dropdown_header` and `draw.dropdown_options`).
- [x] Implement `Dropdown` class (value, `handle_event`, `draw`).
- [x] Add a `DropdownConfig` default config model.
- [x] Wire `Dropdown` into `GUIPanel.add_dropdown` for automatic layout.

## 2. Button interaction polish

- [x] Add a "pressed" visual variant to `draw.button` (e.g. depressed border effect).
- [x] Trigger the pressed visual on `MOUSEBUTTONDOWN`, revert on `MOUSEBUTTONUP` or pointer leave.
- [x] Add a hover state visual (highlight on mouse-over, before a click).

## 3. Style system (`set_style`)

See `docs/style_design.md` for the full design.

- [x] Remove the current (Minecraft-based) look and its config values from the codebase, and `gui_config_models.py` with it.
- [x] Define the style dataclasses in `styles/models.py`: `ButtonStyle`, `SliderStyle`, `DropdownStyle` and `PanelStyle`, grouped in `Style` with the behaviour switches (`hover`, `press_bevel`, `rounded`) and their tuning fields.
- [x] Add `errors.py` with `StyleNotFoundError`.
- [x] Add `DEFAULT_STYLE` to `constants.py`.
- [x] Implement `"embossed"` style (default) — raised 3D buttons with light/dark bevels.
- [x] Implement `"flat"` style — no borders or bevels, hover off.
- [x] Implement `"chalk"` style — dark background, muted tones, rounded corners.
- [x] Implement `"terminal"` style — monospace font (`SysFont` with common monospace names), green on black.
- [x] Implement `"soft"` style — light pastel colours, subtle shadows.
- [x] Implement `set_style()` and the style registry. It sets the active global style, which applies to all controls and draw calls, including ones created before the call.
- [x] Controls, draw functions and `GUIPanel` read the active style at draw and event time. Explicit arguments given at construction are permanent overrides for that control, while `set_style()` changes every other setting.
- [x] Tests: every style sets every field, and an unknown style name raises `StyleNotFoundError`. Checks over every registered style run automatically, so new styles are covered.

## 4. Layout mode system (dropped)

Dropped. Controls are placed either manually on the pygame window or through `GUIPanel`, and no other layouts are planned. A global `set_mode()` was rejected: with only one layout it adds indirection without benefit, and it conflicts with using several panels at once.

## 5. Top-level ergonomic API

- [x] Decide the public API surface for `src/pg_plonker/__init__.py`.
- [x] Export `Button`, `Dropdown`, `Slider`, `GUIPanel`, and `draw` from `__init__.py`.
- [x] Document the `import pg_plonker as pgp` convention in `README.md`.
- [x] Export `set_style` from `__init__.py`.
- [x] Add an `__all__` list to `__init__.py` to make the public surface explicit.

## 6. PyPI publishing

- [ ] Choose and register the package name on PyPI.
- [ ] Add classifiers, license, and author metadata to `pyproject.toml`.
- [ ] Write `CHANGELOG.md`.
- [ ] Set up a build & publish workflow (e.g. GitHub Actions).
- [ ] Publish the initial `0.1.0` release.

---

## Backlog

### Must have

- [ ] Text that is wider than its control overflows or gets cut off. This applies to every element that shows text: the Button label, the Dropdown header and option labels, and the Slider label. Choose one policy (shrink the font to fit, truncate with an ellipsis, or wrap onto several lines) and apply it to all of them.

### Nice to have

- [ ] Keyboard support: a focus system in `GUIPanel` (Tab/Shift+Tab with a focus indicator), Space/Enter to toggle a focused `Button`, arrow keys to step a `Slider`, and Enter/Space to open, arrow keys to move, Enter to select and Escape to close a `Dropdown`.
- [ ] Pick or source a click sound effect asset.
- [ ] Play the sound on toggle inside `Button.handle_event`.
- [ ] Add a way to mute/disable sound globally.