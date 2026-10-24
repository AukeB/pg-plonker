"""Module for the custom exceptions raised by pg-plonker.

Classes: - StyleNotFoundError: Raised when no style is registered under the
given name.
"""


class StyleNotFoundError(Exception):
    """Raised when set_style() is given a name that no style is registered
    under.
    """
