import json
import random
import time

from PIL import Image, ImageFont, ImageDraw
from vk_getter.utils import download_from_url

from utils import get_cat_photos_urls, Shape, shape_crop


if __name__ == "__main__":
    #cats = get_cat_photos_urls()
    #with open("static/urls/cats.json", "w") as f:
    #    json.dump(cats, f, indent=4)

    with open("static/urls/cats.json", "r") as f:
        cats = json.load(f)

    random_cat = random.choice(cats)
    print(random_cat)
    response = download_from_url(random_cat, ".", "cat")

    img = shape_crop("cat.jpeg", Shape.heart)
    background = Image.open("./static/images/background2.png")
    background.paste(img, (300, 550), img)
    text = u"  Ты моя любимка"
    font = ImageFont.truetype("./static/fonts/BryndanWriteBook.ttf", 150)
    draw = ImageDraw.Draw(background)
    draw.text((150, 350), text, font=font)
    draw.text((300, 1600), text="мое солнышко :)", font=font)
    background.show()
    background.save("./static/images/result.png", "PNG")
