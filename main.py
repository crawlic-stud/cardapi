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
    with open("static/urls/dogs.json", "r") as f:
        animals = json.load(f)

    random_animal = random.choice(animals)

    width, height = 1000, 1200
    card = Card(random_animal, (width, height))

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
            Palette(
                # *get_colors(card.image, 3),
                # *get_colors(card.image, 2),
            )
        ) \
        .change_background() \
        .add_outline(150) \
        .scale_image(0.75) \
        .move_image(150) \
        .set_font(Font.variant_1) \
        .add_title("я хочу дарувати тобi тепло кожен день!") \
        .add_text("спасибi, що змушуеш мене посмiхатися i відчувати себе живою! ти робиш мое життя яскравим i незабутнiм! давай будемо поруч один з одним завжди!") \
        .save_image("./static/images/result.png")
        