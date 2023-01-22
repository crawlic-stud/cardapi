from typing import Union
import pathlib
import io

from PIL import Image
from requests.exceptions import MissingSchema

from .background import Background
from .palette import Palette
from utils.crop import Shape, shape_crop
from utils.functions import get_bytes_from_url

ImageType = Union[Image.Image, str, pathlib.Path]


def init_image(image: ImageType) -> Image.Image:
    if isinstance(image, str):
        try:
            image_bytes = get_bytes_from_url(image)
            image = Image.open(io.BytesIO(image_bytes))
        except MissingSchema:
            image_path = pathlib.Path(image)
            image = Image.open(image_path)            
    return image


def get_center(bg, image):
    x = (bg.width - image.width) // 2
    y = (bg.height - image.height) // 2
    return x, y


class Card:
    """Class to chain create card images."""
    def __init__(
        self, 
        image: ImageType,
        size: tuple[int, int],
    ):
        self.size = size
        self.image = init_image(image)
        self.shape = None
        self.bg_image = None
        self.palette = None

    def shape_image(self, shape: Shape, scale_factor: int = 0.75):
        self.image = shape_crop(self.image, shape, scale_factor)
        self.shape = shape
        return self

    def scale_image(self, factor):
        self.image = self.image.resize((
            int(self.image.width * factor),
            int(self.image.height * factor),
        ))
        return self

    def add_palette(self, palette: Palette):
        self.palette = palette
        return self

    def add_background(self, blur: int = 250, opacity: float = 0.0):
        if self.palette is None:
            raise ValueError("You should add palette first.")
        bg = Background(self.palette, *self.size, blur)
        self.bg_image = bg.random(opacity)
        return self

    def add_outline(self, width: int, blur: int = 250):
        if self.bg_image is None:
            raise ValueError("You should add background first.")
        if self.shape is None:
            raise ValueError("You should shape image first.")

        outline_img_size = self.image.width + width, self.image.height + width
        outline_img = Background(
            self.palette, *outline_img_size, blur
        ).outline()

        x, y = get_center(outline_img, self.image)
        outline_img.paste(self.image, (x, y), self.image)
        outline_img = shape_crop(outline_img, self.shape, 1)
        self.image = outline_img.resize(self.image.size)
        return self
        
    def _get_image(self):
        img = self.bg_image
        x, y = get_center(img, self.image)
        img.paste(self.image, (x, y), self.image)
        return img

    def show_image(self):
        img = self._get_image()
        img.show()
        return self

    def save_image(self, path: Union[str, pathlib.Path], format_: str = "PNG"):
        img = self._get_image()
        img.save(path, format_)
        return self
