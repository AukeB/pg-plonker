"""Project-specific constants."""

# Determines the ratio between the PyGame window resolution and the screen resolution
WINDOW_SIZE_SCREEN_FRACTION = 0.9

# Name of the style that is active until set_style() is called.
# Must be a name registered in pg_plonker/styles/registry.py. Available styles:
#   "chalk"
#   "embossed"
#   "flat"
#   "soft"
#   "terminal"
DEFAULT_STYLE = "embossed"
