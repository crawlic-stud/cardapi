from typing import Union, Optional

from dataclasses import dataclass


Color = Optional[Union[str, tuple[int, int, int]]]


@dataclass
class Palette:
    """Palette class for storing all colors in a card."""
    background_color: Color = (0, 0, 0) # black
    primary_color: Color = None
    secondary_color: Color = None
    accent_color: Color = (255, 255, 255) # white
    additional_color: Color = None

    def __post_init__(self):
        if self.primary_color is None:
            self.primary_color = self.background_color
        if self.secondary_color is None:
            self.secondary_color = self.primary_color
        if self.additional_color is None:
            self.additional_color = self.accent_color
