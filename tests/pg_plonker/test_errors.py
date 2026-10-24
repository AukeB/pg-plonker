"""Tests for the errors module."""

import pytest

from pg_plonker.errors import StyleNotFoundError

# Testing the "StyleNotFoundError" class.


def test_style_not_found_error_carries_its_message() -> None:
    with pytest.raises(StyleNotFoundError, match="no-such-style"):
        raise StyleNotFoundError("no-such-style")
