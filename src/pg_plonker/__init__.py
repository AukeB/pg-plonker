"""Public API of pg-plonker.

Importing the package exposes the controls, the panel, the stateless drawing
module, and the config models, so user code can write ``import pg_plonker as
pgp`` and then use ``pgp.Button``, ``pgp.GUIPanel``, or ``pgp.draw``.

Modules:
- draw: Stateless pygame drawing functions for UI elements.
- controls: Stateful controls (Button, Slider, Dropdown).
- gui_panel: The GUIPanel control container.
- gui_config_models: Default configuration models for the controls and panel.
"""

from pg_plonker import draw
from pg_plonker.controls import Button, Dropdown, Slider
from pg_plonker.gui_config_models import (
    ButtonConfig,
    DropdownConfig,
    GUIPanelConfig,
    SliderConfig,
)
from pg_plonker.gui_panel import GUIPanel

__all__ = [
    "Button",
    "ButtonConfig",
    "Dropdown",
    "DropdownConfig",
    "GUIPanel",
    "GUIPanelConfig",
    "Slider",
    "SliderConfig",
    "draw",
]
