from models.preset import Preset
from models.image_text import ImageText

color = (255, 0, 255)
text = ' Ты самая классная самая лучшая самая красивая спасибо что ты есть\n\nТы солнышко мое мой лучик света!'
font = './static/fonts/BryndanWriteBook.ttf'
img = ImageText((800, 600), font, Preset.NEON)


def main():
    y = 100
    result = img.write_title(
        (None, y), "Моей девушке!", max_height=50, max_width=600
    )
    if not result:
        return

    result = img.write_additional_text(
        (100, y + result[1]), text * 7, box_width=600, font_size=11, place="center")
    img.image.save('sample-imagetext.png')


main()