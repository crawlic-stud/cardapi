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
    new_img = image.resize((int(new_width), int(new_height)))
    return new_img


def smart_crop(image):
    """Smart crops an image into a rectangular shape"""

    cropper = SmartCrop()
    # scale by factor to make it look better
    size = int(min(image.width, image.height) * 0.75)
    result = cropper.crop(image, size, size)

    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['width'] + result['top_crop']['x'],
        result['top_crop']['height'] + result['top_crop']['y']
    )

    cropped_image = image.crop(box).convert("RGBA")
    return cropped_image


def shape_crop(img_path, shape_name):
    """Crops images into chosen shape.

    Available shapes: blob, circle, cloud, diamond, door, flag, heart, party, polygon, softstar, star.
    """

    # load images
    image = Image.open(img_path).convert("RGB")
    shape = Image.open(f"./static/shapes/{shape_name}.png")

    # smart crop image
    image = smart_crop(image)
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


if __name__ == "__main__":
    img = shape_crop("kit2.png", Shape.heart)
    background = Image.open("./static/images/background.png")
    background.paste(img, (250, 100), img)
    text = u"Прива !"
    font = ImageFont.truetype("./static/fonts/BryndanWriteBook.ttf", 200)
    draw = ImageDraw.Draw(background)
    draw.text((250, 1250), text, font=font)
    background.show()
    background.save("./static/images/result.png", "PNG")
