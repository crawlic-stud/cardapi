from typing import Union
import pathlib
import io

from PIL import Image
from requests.exceptions import MissingSchema

from .background import Background
from .palette import Palette
from .preset import Preset
from .image_text import ImageText
from .font import Font
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
        self.processed_image = self.image
        self.shape = Shape.CIRCLE
        self.palette = Preset.NEON
        self.bg_image = Background(self.palette, *size).random()
        self.image_position = get_center(self.bg_image, self.image)
        self.image_text = ImageText(size, Font.variant_1, self.palette)
        self._font_size = 36
        self._title_height = 100
        self._padding_x = 50
        self._title_y_pos = 0

    def shape_image(self, shape: Shape, scale_factor: int = 0.75):
        self.image = shape_crop(self.image, shape, scale_factor)
        self.shape = shape
        return self

    def scale_image(self, factor):
        self.processed_image = self.processed_image.resize((
            int(self.processed_image.width * factor),
            int(self.processed_image.height * factor),
        ))
        return self

    def change_palette(self, palette: Palette):
        self.palette = palette
        return self

    def change_background(self, blur: int = 250, opacity: float = 0.0):
        bg = Background(self.palette, *self.size, blur)
        self.bg_image = bg.random(opacity)
        return self

    def add_outline(self, width: int, blur: int = 250):
        outline_img_size = (
            self.image.width + width, 
            self.image.height + width
        )
        outline_img = Background(
            self.palette, *outline_img_size, blur
        ).outline()
        x, y = get_center(outline_img, self.image)
        outline_img.paste(self.image, (x, y), self.image)
        outline_img = shape_crop(outline_img, self.shape, 1)
        self.processed_image = outline_img.resize(self.image.size)
        return self

    def _get_position(self):
        if self.image_position is None:
            return get_center(self.bg_image, self.processed_image)
        return self.image_position

    def move_image(self, amount: int = 100):
        x, y = get_center(self.bg_image, self.processed_image)
        y -= amount
        self.image_position = x, y
        return self

    def _get_image(self):
        img = self.bg_image
        x, y = self._get_position()
        img.paste(self.image_text.image, (0, 0), self.image_text.image)
        img.paste(self.processed_image, (x, y), self.processed_image)
        return img

    def show_image(self):
        img = self._get_image()
        img.show()
        return self

    def save_image(self, path: Union[str, pathlib.Path], format_: str = "PNG"):
        img = self._get_image()
        img.save(path, format_)
        return self

    def get_image_bytes(self):
        img = self._get_image()
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def set_font(self, font: Font):
        self.image_text = ImageText(self.size, font, self.palette)
        return self
        
    def _calculate_title_y(self, padding: int):
        _, img_y = self._get_position()
        y_pos = img_y + self.processed_image.height + padding
        return y_pos
    
    def set_title_height(self, height: int):
        self._title_height = height
        return self

    def set_padding_x(self, padding: int):
        self._padding_x = padding
        return self
    
    def set_font_size(self, size: int):
        self._font_size = size
        return self
    
    def add_title(self, text: str, padding: int = 10):
        width = self.size[0]
        y_pos = self._calculate_title_y(padding)
        self._title_y_pos = y_pos
        result = self.image_text.write_title(
            pos=(None, y_pos), 
            text=text, 
            max_height=self._title_height, 
            max_width=width - self._padding_x * 2,
        )
        if result:
            self._title_y_pos += result[1]
        return self

    def add_text(self, text: str, padding: int = 10, place: str = "center"):
        width = self.size[0]
        y_pos = padding + self._title_y_pos
        self.image_text.write_additional_text(
            pos=(self._padding_x, y_pos),
            text=text,
            font_size=self._font_size,
            box_width=width - self._padding_x * 2,
            place=place,
        )
        return self
