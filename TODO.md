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

- [x] `ButtonConfig` default config model.
- [x] `GUIPanelConfig` default config model.
- [x] Removed unused `PGPlonkerConfig` aggregate.

### Utilities

- [x] Font caching (`get_font`) to avoid repeated `pg.font.SysFont` calls.
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
- [ ] Design `Dropdown` control API (options list, selected value, open/closed state).
- [ ] Implement `draw.dropdown` stateless drawing function.
- [ ] Implement `Dropdown` class (value, `handle_event`, `draw`).
- [ ] Add a `DropdownConfig` default config model.
- [ ] Wire `Dropdown` into `GUIPanel.add_dropdown` for automatic layout.

## 2. Button interaction polish

- [ ] Add a "pressed" visual variant to `draw.button` (e.g. depressed border effect).
- [ ] Trigger the pressed visual on `MOUSEBUTTONDOWN`, revert on `MOUSEBUTTONUP` or pointer leave.
- [ ] Add a hover state visual (highlight on mouse-over, before a click).
- [ ] Pick or source a click sound effect asset.
- [ ] Play the sound on toggle inside `Button.handle_event`.
- [ ] Add a way to mute/disable sound globally.

## 3. Style system (`set_style`)

- [ ] Design a style/theme data structure mapping style name → config values per control.
- [ ] Implement `"embossed"` style — raised 3D buttons with light/dark inner borders creating depth.
- [ ] Implement `"flat"` style — clean, minimal, no borders or shadows.
- [ ] Implement `"chalk"` style — dark background with soft, muted tones and a rounded feel.
- [ ] Implement `"terminal"` style — monospace font, green on black, CLI-inspired.
- [ ] Implement `"soft"` style — light pastel colors, subtle shadows, friendly and modern.
- [ ] Implement `set_style()` to set the active global style before creating controls.
- [ ] Support per-control overrides after `set_style` has been applied.

## 4. Layout mode system (`set_mode`)

- [ ] Define a common `Mode` interface/protocol that layout containers implement.
- [ ] Refactor `GUIPanel` to conform to the `Mode` interface.
- [ ] Implement `set_mode()` to select and activate a mode.
- [ ] Decouple adding controls from being hardcoded to `GUIPanel` specifically.
- [ ] Design how mode-specific config (e.g. `GUIPanelConfig`) gets passed through `set_mode()`.
- [ ] Support multiple simultaneously active modes/panels (e.g. a left and a right panel).

## 5. Top-level ergonomic API

- [ ] Decide the public API surface for `src/pg_plonker/__init__.py`.
- [ ] Export `Button`, `GUIPanel`, `draw`, and the config models from `__init__.py`.
- [ ] Document the `import pg_plonker as pgp` convention in `README.md`.
- [ ] Export `set_style` / `set_mode` from `__init__.py` once implemented.
- [ ] Add an `__all__` list to `__init__.py` to make the public surface explicit.

## 6. PyPI publishing

- [ ] Choose and register the package name on PyPI.
- [ ] Add classifiers, license, and author metadata to `pyproject.toml`.
- [ ] Write `CHANGELOG.md`.
- [ ] Set up a build & publish workflow (e.g. GitHub Actions).
- [ ] Publish the initial `0.1.0` release.