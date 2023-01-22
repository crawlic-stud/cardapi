from models.preset import Preset
from image_utils import ImageText

color = (255, 0, 255)
text = 'Ты самая классная самая лучшая самая красивая спасибо что ты есть\n\nТы солнышко мое мой лучик света!'
font = './static/fonts/BryndanWriteBook.ttf'
img = ImageText((800, 600), font, Preset.GREEN)

#write_text_box will split the text in many lines, based on box_width
#`place` can be 'left' (default), 'right', 'center' or 'justify'
#write_text_box will return (box_width, box_calculed_height) so you can
#know the size of the wrote text

img.write_text_box((300, 50), text * 1, box_width=200,
                   font_size=15, color=color, place="right")

# You don't need to specify text size: can specify max_width or max_height
# and tell write_text to fill the text in this space, so it'll compute font
# size automatically
#write_text will return (width, height) of the wrote text
img.write_text(None, "Python is a cool programming language.", 
                max_height=250, max_width=600, color=color)

img.background.save('sample-imagetext.png')
