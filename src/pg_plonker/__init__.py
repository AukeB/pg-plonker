"""Public API of pg-plonker.

Importing the package exposes the controls, the panel, the stateless drawing
module, and set_style(), so user code can write ``import pg_plonker as pgp`` and
then use ``pgp.Button``, ``pgp.GUIPanel``, ``pgp.draw`` or ``pgp.set_style``.

Modules:
- draw: Stateless pygame drawing functions for UI elements.
- controls: Stateful controls (Button, Slider, Dropdown).
- gui_panel: The GUIPanel control container.
- styles: Style definitions and set_style().
"""

from pg_plonker import draw
from pg_plonker.controls import Button, Dropdown, Slider
from pg_plonker.gui_panel import GUIPanel
from pg_plonker.styles import set_style

__all__ = [
    "Button",
    "Dropdown",
    "GUIPanel",
    "Slider",
    "draw",
    "set_style",
]
