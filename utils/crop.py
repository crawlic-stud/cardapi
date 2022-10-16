from turtle import back
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from smartcrop import SmartCrop

import io
from enum import Enum


class Shape:
    blob: str = "blob"
    circle: str = "circle"
    cloud: str = "cloud"
    diamond: str = "diamond"
    door: str = "door"
    flag: str = "flag"
    heart: str = "heart"
    party: str = "party"
    polygon: str = "polygon"
    softstar: str = "softstar"
    star: str = "star"


def get_mask(img_array):
    """Create mask from every black pixel on the image."""
    filter_color = np.array([255] * img_array.shape[-1])
    mask = np.where(np.all(img_array == filter_color, axis=-1), 1, 0)
    return mask


def apply_mask(img_array, mask):
    """Applies mask on image array."""
    mask_rgb = np.stack((mask,) * img_array.shape[-1], axis=-1)
    result = img_array * mask_rgb
    return np.array(result, dtype=np.uint8)


def scale_image(image, width, height):
    """Scales image."""
    wx = width / image.width if width > image.width else image.width / width
    hx = height / image.height if height > image.height else image.height / width
    factor = max(wx, hx)
    new_width, new_height = image.width * factor, image.height * factor
    new_img = image.resize((round(new_width), round(new_height)))
    return new_img


def smart_crop(image, factor=0.75):
    """Smart crops an image into a rectangular shape"""

    max_size = 800
    if image.width > max_size or image.height > max_size:
        factor = max(image.width, image.height) / max_size
        new_width = image.width // factor
        new_height = image.height // factor
        image = image.resize((int(new_width), int(new_height)))

    cropper = SmartCrop()

    # scale by factor to make it look better
    size = int(min(image.width, image.height) * factor)
    result = cropper.crop(image, size, size)

    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['width'] + result['top_crop']['x'],
        result['top_crop']['height'] + result['top_crop']['y']
    )

    cropped_image = image.crop(box).convert("RGBA")
    return cropped_image


def shape_crop(img_path, shape_name, factor=1):
    """Crops images into chosen shape.

    Available shapes: blob, circle, cloud, diamond, door, flag, heart, party, polygon, softstar, star.
    """

    # load images
    image = Image.open(img_path).convert("RGB")
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


def get_bytes(image):
    """Returns image as byte array"""

    byte_array = io.BytesIO()
    image.save(byte_array, format="PNG")
    return byte_array.getvalue()    
