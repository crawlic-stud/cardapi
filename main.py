import json
import random

from PIL import Image

from utils import Shape
from models import Palette, Card, Preset
from models.font import Font


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

    width, height = 1000, 1200
    # print(random_animal)
    # card = Card(random_animal, (width, height))
    card = Card("static/images/elmira.JPG", (width, height))

    card \
        .shape_image(Shape.HEART) \
        .change_palette( 
            # Palette(
            #     (184, 238, 255),
            #     (120, 248, 255),
            #     (191, 255, 207),
            #     (19, 127, 173),
            #     (30, 129, 138),
            # )
            # Palette(
            #     (255, 214, 234),
            #     (253, 222, 255),
            #     (236, 156, 255),
            #     (138, 37, 99),
            #     (168, 57, 83),
            # )
            # Palette(
            #     (255, 232, 253),
            #     (255, 112, 203),
            #     (255, 145, 198),
            #     (115, 18, 28),
            #     (161, 34, 95),
            # )
            # Palette(
            #     (255, 234, 186),
            #     (252, 172, 204),
            #     (255, 189, 158),
            #     (194, 56, 17),
            #     (217, 102, 20),
            # )
            # Palette(
            #     (191, 234, 255),
            #     (161, 255, 222),
            #     (192, 228, 252),
            #     (112, 115, 255),
            #     (109, 166, 252),
            # )
            # Palette(
            #     (252, 212, 239),
            #     (252, 224, 220),
            #     (252, 167, 185),
            #     (217, 98, 139),
            #     (240, 117, 144),
            # )
            Palette(
                (255, 130, 174),
                (255, 220, 173),
                (252, 169, 157),
                (255, 56, 79),
                (235, 122, 70),
            )
        ) \
        .change_background() \
        .add_outline(150) \
        .scale_image(0.75) \
        .move_image(150) \
        .set_font(Font.variant_5) \
        .set_font_size(42) \
        .set_padding_x(120) \
        .add_title("Любимой тёте Эльмирочке!", padding=20) \
        .set_padding_x(200) \
        .add_text("Как много разных валентинок Кружится в снежном феврале. \nОдна из них — моя к тебе!", 
                  padding=0) \
        .save_image("./static/images/result.png") \
        .show_image()
        