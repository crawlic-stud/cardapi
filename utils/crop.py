from typing import Union

from PIL import Image
import numpy as np
from smartcrop import SmartCrop

import io


class Shape:
    BLOB: str = "blob"
    CIRCLE: str = "circle"
    CLOUD: str = "cloud"
    DIAMOND: str = "diamond"
    DOOR: str = "door"
    FLAG: str = "flag"
    HEART: str = "heart"
    PARTY: str = "party"
    POLYGON: str = "polygon"
    SOFTSTAR: str = "softstar"
    STAR: str = "star"


def get_mask(img_array: np.array) -> np.array:
    """Create mask from every black pixel on the image."""
    filter_color = np.array([255] * img_array.shape[-1])
    mask = np.where(np.all(img_array == filter_color, axis=-1), 1, 0)
    return mask


def apply_mask(img_array: np.array, mask: np.array) -> np.array:
    """Applies mask on image array."""
    mask_rgb = np.stack((mask,) * img_array.shape[-1], axis=-1)
    result = img_array * mask_rgb
    return np.array(result, dtype=np.uint8)


def scale_image(image: Image.Image, width: int, height: int) -> Image.Image:
    """Scales image."""
    wx = width / image.width if width > image.width else image.width / width
    hx = height / image.height if height > image.height else image.height / width
    factor = max(wx, hx)
    new_width, new_height = image.width * factor, image.height * factor
    new_img = image.resize((round(new_width), round(new_height)))
    return new_img


def smart_crop(image: Image.Image, factor: int = 0.75) -> Image.Image:
    """Smart crops an image into a rectangular shape, scaling it down by factor"""

    max_size = 800
    if image.width > max_size or image.height > max_size:
        factor = max(image.width, image.height) / max_size
        new_width = image.width // factor
        new_height = image.height // factor
        image = image.resize((int(new_width), int(new_height)))

    cropper = SmartCrop()

    # scale by factor to make it look better
    size = int(min(image.width, image.height) * factor)
    image = image.convert("RGB")
    result = cropper.crop(image, size, size)

    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['width'] + result['top_crop']['x'],
        result['top_crop']['height'] + result['top_crop']['y']
    )

    cropped_image = image.crop(box).convert("RGBA")
    return cropped_image


def shape_crop(image: Union[str, Image.Image], shape_name: Union[str, Shape], factor: int = 1) -> Image.Image:
    """Crops images into chosen shape.

    Available shapes: blob, circle, cloud, diamond, door, flag, heart, party, polygon, softstar, star.
    """

    # check if shape_name is valid
    getattr(Shape, shape_name.upper())  

    # load images
    if isinstance(image, str):
        image = Image.open(image).convert("RGB")
    shape = Image.open(f"./static/shapes/{shape_name}.png")

    # smart crop image
    image = smart_crop(image, factor)
    image = scale_image(image, shape.width, shape.height)

    # get arrays for both images
    img_array = np.array(image)
    shape_array = np.array(shape)

    # get and apply mask
    mask = get_mask(shape_array)

    applied_mask = apply_mask(img_array, mask)

    result_img = Image.fromarray(applied_mask)
    result_img = result_img.resize(
        (shape.width // 2, shape.height // 2), resample=Image.ANTIALIAS)

    return result_img


def get_bytes(image: Image.Image) -> bytes:
    """Returns image as byte array"""

    byte_array = io.BytesIO()
    image.save(byte_array, format="PNG")
    return byte_array.getvalue()    
