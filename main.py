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
    print(random_animal)
    card = Card(random_animal, (width, height))
    # card = Card("https://sun9-77.userapi.com/impg/r5KBGSWhIemSFRquNd5m4f4El_gYFQr6QBb1HQ/AwUp14Pn7sk.jpg?size=694x693&quality=96&sign=6115c30399f7e452dcede64ae91e0259&c_uniq_tag=rjg2sjwFq_sCuFzNAiVfHKIx7_k0ETVFqH2qTA4l4H8&type=album", (width, height))

    card \
        .shape_image(Shape.HEART) \
        .change_palette( 
            Palette(
                (184, 238, 255),
                (120, 248, 255),
                (191, 255, 207),
                (19, 127, 173),
                (30, 129, 138),
            )
            # Palette(
            #     (255, 214, 234),
            #     (253, 222, 255),
            #     (236, 156, 255),
            #     (138, 37, 99),
            #     (168, 57, 83),
            # )
        ) \
        .change_background() \
        .add_outline(150) \
        .scale_image(0.75) \
        .move_image(125) \
        .set_font(Font.variant_5) \
        .set_font_size(32) \
        .add_title("я хочу дарувати тобi тепло кожен день!", padding=20) \
        .add_text("дякую, що змушуеш мене посмiхатися i вiдчувати себе живою! ти робиш мое життя яскравим i незабутнiм! давай будемо поруч один з одним завжди!", 
                  padding=0) \
        .save_image("./static/images/result.png")
        