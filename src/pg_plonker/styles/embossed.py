"""Module for the embossed style, the default style.

Constants: - EMBOSSED: The embossed style, with raised 3D controls and
light/dark bevels.
"""

from pg_plonker.styles.models import (
    ButtonStyle,
    DropdownStyle,
    PanelStyle,
    SliderStyle,
    Style,
)

EMBOSSED = Style(
    button=ButtonStyle(
        font_name="arial",
        font_size=50,
        width=540,
        height=108,
        border_width=5,
        border_width_inner=3,
        text_shadow_offset=3,
        color_background_active=(150, 150, 150),
        color_background_inactive=(210, 210, 210),
        color_text=(30, 30, 30),
        color_border=(40, 40, 40),
        color_border_inner_light=(255, 255, 255),
        color_border_inner_dark=(90, 90, 90),
        color_text_shadow=(255, 255, 255),
    ),
    slider=SliderStyle(
        font_name="arial",
        font_size=28,
        width=540,
        height=12,
        handle_radius=16,
        border_width=3,
        margin_vertical=24,
        extra_decimal_places=2,
        color_track=(170, 170, 170),
        color_track_filled=(120, 120, 120),
        color_handle=(230, 230, 230),
        color_border=(40, 40, 40),
        color_text=(30, 30, 30),
    ),
    dropdown=DropdownStyle(
        font_name="arial",
        font_size=32,
        width=540,
        height=72,
        option_height=60,
        border_width=5,
        border_width_inner=3,
        text_shadow_offset=3,
        arrow_size=14,
        text_padding=12,
        color_background_active=(190, 190, 190),
        color_background_inactive=(200, 200, 200),
        color_background_option=(225, 225, 225),
        color_background_option_hover=(190, 190, 190),
        color_text=(30, 30, 30),
        color_border=(40, 40, 40),
        color_border_inner_light=(255, 255, 255),
        color_border_inner_dark=(90, 90, 90),
        color_text_shadow=(255, 255, 255),
        color_arrow=(40, 40, 40),
    ),
    panel=PanelStyle(
        border_width=2,
        color_background=(235, 235, 235),
        color_border=(40, 40, 40),
    ),
    hover=True,
    hover_lighten=0.15,
    press_bevel=True,
    rounded=False,
    corner_radius=0,
)
