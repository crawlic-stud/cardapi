from dataclasses import dataclass


@dataclass
class Palette:
    """Palette class for storing all colors in a card."""
    background_color: str | tuple[int, int, int] = (0, 0, 0) # black
    primary_color: str | tuple[int, int, int] | None = None
    secondary_color: str | tuple[int, int, int] | None = None
    accent_color: str | tuple[int, int, int] | None = (255, 255, 255) # white
    additional_color: str | tuple[int, int, int] | None = None

    def __post_init__(self):
        if self.primary_color is None:
            self.primary_color = self.background_color
        if self.secondary_color is None:
            self.secondary_color = self.primary_color
        if self.additional_color is None:
            self.additional_color = self.accent_color
