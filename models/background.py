import random
from dataclasses import dataclass

from PIL import Image, ImageFilter, ImageDraw

from .palette import Palette


@dataclass
class Background:
    """Class for creating various background images."""
    palette: Palette
    width: int
    height: int
    blur: int = 250

    def _create_bg_draw(self, color=None):
        if color is None:
            color = self.palette.background_color
        bg = Image.new("RGBA", (self.width, self.height), color)
        draw = ImageDraw.Draw(bg)
        return bg, draw

    def _get_random_point(self):
        center = random.randint(0, self.width), random.randint(0, self.height)
        return center

    @staticmethod
    def _draw_circle(draw, cx, cy, radius, color):
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)

    def random(self, opacity: float = 0):
        """Returns random blurred image with randomly spreaded circles."""

        if not 0 <= opacity < 1:
            raise ValueError("Opacity must be between 0 and 1.")

        bg, draw = self._create_bg_draw()

        big_radius = max(self.width, self.height) // 2
        small_radius = max(self.width, self.height) // 4

        self._draw_circle(
            draw, *self._get_random_point(), big_radius, self.palette.primary_color
        )

        for _ in range(2):
            self._draw_circle(
                draw, *self._get_random_point(), small_radius, self.palette.secondary_color
            )

        bg = bg.filter(ImageFilter.BoxBlur(self.blur))

        if opacity:
            white_mask = Image.new("RGBA", bg.size, (255, 255, 255, int(opacity * 255)))
            bg.alpha_composite(white_mask)

        return bg

    def circles(self):
        """Returns blurred circles image on top of each other in the center."""
        
        bg, draw = self._create_bg_draw()
        cx, cy = self.width // 2, self.height // 2
        radius = min(self.width, self.height) // 2

        self._draw_circle(draw, cx, cy, radius, self.palette.secondary_color)
        self._draw_circle(draw, cx, cy, radius // 1.5, self.palette.primary_color)

        bg = bg.filter(ImageFilter.BoxBlur(self.blur))
        return bg
    
    def outline(self):
        """Creates random background for outline."""
        
        bg, draw = self._create_bg_draw(self.palette.accent_color)
        radius = min(self.width, self.height)

        for _ in range(5):
            self._draw_circle(
                draw, *self._get_random_point(), radius // 5, self.palette.additional_color
            )

        bg = bg.filter(ImageFilter.BoxBlur(self.blur))
        return bg
