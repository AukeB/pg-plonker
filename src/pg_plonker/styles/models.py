"""Module for the style dataclasses that every style fills in.

The shape is a tree. Style is the root, and every style module (for example
styles/embossed.py) builds one Style instance:

- Style groups one instance of each element dataclass in its button, slider,
  dropdown and panel fields. It also holds the behaviour switches (hover,
  press_bevel, rounded) that apply across elements.
- ButtonStyle, SliderStyle and DropdownStyle hold the values read by the Button,
  Slider and Dropdown controls and by their draw functions (draw.button,
  draw.slider, draw.dropdown_header and draw.dropdown_options).
- PanelStyle holds the visual values read by GUIPanel. Its layout arguments
  (width, margins, alignment) are constructor arguments, not style values.

Controls and draw functions get their values by walking from get_style() down
this tree, for example get_style().button.width. Every field of the element
dataclasses is required, so a style cannot leave an element partly defined.

Classes:
- ButtonStyle: The values a style sets for Button and draw.button.
- SliderStyle: The values a style sets for Slider and draw.slider.
- DropdownStyle: The values a style sets for Dropdown and the dropdown draw
  functions.
- PanelStyle: The visual values a style sets for GUIPanel.
- Style: The full set of values for one style, grouping the four elements and
  the behaviour switches.

Type aliases: RGBColor: An (red, green, blue) color tuple.
"""

from dataclasses import dataclass

type RGBColor = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonStyle:
    """The values a style sets for Button and draw.button.

    Attributes:
        font_name (str): System font name for the label.
        font_size (int): Font size of the label in points.
        width (int): Button width in pixels.
        height (int): Button height in pixels.
        border_width (int): Outer border thickness.
        border_width_inner (int): Inner bevel thickness.
        text_shadow_offset (int): Offset of the label shadow.
        color_background_active (RGBColor): Background when on.
        color_background_inactive (RGBColor): Background when off.
        color_text (RGBColor): Label colour.
        color_border (RGBColor): Outer border colour.
        color_border_inner_light (RGBColor): Light bevel colour.
        color_border_inner_dark (RGBColor): Dark bevel colour.
        color_text_shadow (RGBColor): Label shadow colour.
    """

    font_name: str
    font_size: int
    width: int
    height: int
    border_width: int
    border_width_inner: int
    text_shadow_offset: int
    color_background_active: RGBColor
    color_background_inactive: RGBColor
    color_text: RGBColor
    color_border: RGBColor
    color_border_inner_light: RGBColor
    color_border_inner_dark: RGBColor
    color_text_shadow: RGBColor


@dataclass(frozen=True)
class SliderStyle:
    """The values a style sets for Slider and draw.slider.

    Attributes:
        font_name (str): System font name for the value readout.
        font_size (int): Font size of the value readout in points.
        label_font_size (int): Font size of the label in points.
        width (int): Track width in pixels.
        height (int): Track height in pixels.
        handle_radius (int): Handle radius in pixels.
        border_width (int): Handle border thickness.
        padding (int): Space between the box edge and its contents.
        box_border_width (int): Outer border thickness of the box.
        box_border_width_inner (int): Inner bevel thickness of the box.
        color_box_background (RGBColor): Box background colour.
        color_box_border (RGBColor): Box outer border colour.
        color_box_border_inner_light (RGBColor): Box light bevel colour.
        color_box_border_inner_dark (RGBColor): Box dark bevel colour.
        extra_decimal_places (int): Decimal places shown beyond the precision
            implied by start, stop and step.
        color_track (RGBColor): Track colour.
        color_track_filled (RGBColor): Colour of the track left of the handle.
        color_handle (RGBColor): Handle fill colour.
        color_border (RGBColor): Handle border colour.
        color_text (RGBColor): Value readout colour.
    """

    font_name: str
    font_size: int
    label_font_size: int
    width: int
    height: int
    handle_radius: int
    border_width: int
    padding: int
    box_border_width: int
    box_border_width_inner: int
    extra_decimal_places: int
    color_track: RGBColor
    color_track_filled: RGBColor
    color_handle: RGBColor
    color_border: RGBColor
    color_text: RGBColor
    color_box_background: RGBColor
    color_box_border: RGBColor
    color_box_border_inner_light: RGBColor
    color_box_border_inner_dark: RGBColor


@dataclass(frozen=True)
class DropdownStyle:
    """The values a style sets for Dropdown and the dropdown draw functions.

    Attributes:
        font_name (str): System font name for the labels.
        font_size (int): Font size of the labels in points.
        width (int): Header and option width in pixels.
        height (int): Header height in pixels.
        option_height (int): Height of each option row in pixels.
        border_width (int): Outer border thickness.
        border_width_inner (int): Inner bevel thickness.
        text_shadow_offset (int): Offset of the label shadow.
        arrow_size (int): Half-width and height of the arrow.
        text_padding (int): Space between the edge and the label.
        color_background_active (RGBColor): Header background when open.
        color_background_inactive (RGBColor): Header background when closed.
        color_background_option (RGBColor): Option row background.
        color_background_option_hover (RGBColor): Hovered option row background.
        color_text (RGBColor): Label colour.
        color_border (RGBColor): Outer border colour.
        color_border_inner_light (RGBColor): Light bevel colour.
        color_border_inner_dark (RGBColor): Dark bevel colour.
        color_text_shadow (RGBColor): Label shadow colour.
        color_arrow (RGBColor): Arrow colour.
    """

    font_name: str
    font_size: int
    width: int
    height: int
    option_height: int
    border_width: int
    border_width_inner: int
    text_shadow_offset: int
    arrow_size: int
    text_padding: int
    color_background_active: RGBColor
    color_background_inactive: RGBColor
    color_background_option: RGBColor
    color_background_option_hover: RGBColor
    color_text: RGBColor
    color_border: RGBColor
    color_border_inner_light: RGBColor
    color_border_inner_dark: RGBColor
    color_text_shadow: RGBColor
    color_arrow: RGBColor


@dataclass(frozen=True)
class PanelStyle:
    """The visual values a style sets for GUIPanel.

    Layout options such as width and margins are not part of a style. They are
    arguments of GUIPanel.

    Attributes:
        border_width (int): Thickness of the panel divider line.
        color_background (RGBColor): Panel background colour.
        color_border (RGBColor): Panel divider colour.
    """

    border_width: int
    color_background: RGBColor
    color_border: RGBColor


@dataclass(frozen=True)
class Style:
    """The full set of values for one style.

    Every style is one instance of this class, so every style sets the same
    fields. The behaviour switches (hover, press_bevel, rounded) apply across
    elements. Their tuning fields are only read while the switch is on.

    Attributes:
        button (ButtonStyle): Values for Button.
        slider (SliderStyle): Values for Slider.
        dropdown (DropdownStyle): Values for Dropdown.
        panel (PanelStyle): Values for GUIPanel.
        hover (bool): Whether hovered elements change their colour.
        hover_lighten (float): Fraction of the distance to white a hovered
            colour moves. Only read while hover is True.
        press_bevel (bool): Whether a pressed button swaps its bevel colours.
        rounded (bool): Whether elements have rounded corners.
        corner_radius (int): Corner radius in pixels. Only read while rounded is
            True.
    """

    button: ButtonStyle
    slider: SliderStyle
    dropdown: DropdownStyle
    panel: PanelStyle
    hover: bool
    hover_lighten: float
    press_bevel: bool
    rounded: bool
    corner_radius: int
