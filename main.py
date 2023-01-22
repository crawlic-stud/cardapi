import json
import random
import time
from turtle import back

from PIL import Image, ImageFont, ImageDraw
from vk_getter.utils import download_from_url

from utils import get_photos_urls, Shape, shape_crop, DOG_GROUPS, get_bytes
#from utils.background import Background, Preset
from models import Preset, Background, Palette, Card


def get_colors(img, numcolors=10, resize=150):
    # Resize image to speed up processing
    img = img.copy()
    img.thumbnail((resize, resize))

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = []
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    return colors


if __name__ == "__main__":
    with open("static/urls/cats.json", "r") as f:
        animals = json.load(f)

    random_animal = random.choice(animals)

    card = Card(random_animal, (900, 1600))

    card \
        .shape_image(Shape.HEART) \
        .add_palette( 
            Palette(
                (255, 138, 130),
                (240, 122, 255),
                (255, 173, 217),
                (176, 0, 32),
                (134, 28, 255),
            )
        ) \
        .add_background() \
        .add_outline(150) \
        .scale_image(0.75) \
        .save_image("./static/images/result1.png") \
        .add_palette( 
            Palette(
                (255, 138, 130),
                (240, 122, 255),
                (0, 173, 217),
                (176, 0, 32),
                (155, 155, 255),
            )
        ) \
        .add_background() \
        .add_outline(150) \
        .save_image("./static/images/result2.png") 
