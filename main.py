import json
import random
import time
from turtle import back

from PIL import Image, ImageFont, ImageDraw
from vk_getter.utils import download_from_url

from utils import get_photos_urls, Shape, shape_crop, DOG_GROUPS
#from utils.background import Background, Preset
from models import Preset, Background, Palette


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
    # dogs = get_photos_urls(DOG_GROUPS, 5000)
    # with open("static/urls/dogs.json", "w") as f:
    #     json.dump(dogs, f, indent=4)

    with open("static/urls/dogs.json", "r") as f:
        dogs = json.load(f)

    random_animal = random.choice(dogs)
    print(random_animal)

    shape = Shape.HEART

    response = download_from_url(random_animal, ".", "cat")
    img = shape_crop("cat.jpeg", shape, 0.75)

    colors = get_colors(img, 4)[1:]
    print(colors)

    size = 1080, 1080
    # palette = Palette(*colors)
    # palette = Preset.NEON
    palette = Palette(
        (252, 113, 38),
        (245, 193, 71),
        (122, 193, 250),
    )
    bg = Background(palette, *size)
    background = bg.circles()

    x = (background.width - img.width) // 2
    y = (background.height - img.height) // 2
    background.paste(img, (x, y), img)
    text = u"  Ты прекраснее"
    font = ImageFont.truetype("./static/fonts/BryndanWriteBook.ttf", 120)
    draw = ImageDraw.Draw(background)
    # draw.text((50, 100), text, font=font, fill="black")
    # draw.text((50, 500), text="всех котиков :)", font=font, fill="black")
    #background.show()
    background.save("./static/images/result.png", "PNG")
    background = shape_crop("./static/images/result.png", shape)

    size = 1250, 1350
    preset = Background(palette, *size)
    new_bg = preset.random(0.0)
    x = (new_bg.width - img.width) // 2
    y = (new_bg.height - img.height) // 2
    new_bg.paste(background, (x, y), background)
    draw = ImageDraw.Draw(new_bg)
    # draw.text((100, 1100), text=" Люблю подписчиков", font=font, fill=palette.accent_color)
    # draw.text((100, 1200), text="    канала ЙОУ", font=font, fill=palette.accent_color)
    new_bg.save("./static/images/result.png", "PNG")
