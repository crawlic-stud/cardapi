from dataclasses import dataclass
import math

from textwrap import wrap
from PIL import ImageFont, Image, ImageDraw


@dataclass
class Font:
    path: str
    size: int = 50

    def get_font(self, size=None):
        if size is None:
            return ImageFont.truetype(self.path, self.size)
        return ImageFont.truetype(self.path, size)

    def get_bbox(self, start, text, text_size=None):
        image = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox(start, text=text, font=self.get_font(text_size))
        return bbox

    def get_size(self, text, text_size=None):
        bbox = self.get_bbox((0, 0), text, text_size)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def fit_in_bbox(self, bbox, text):
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        text_bbox = self.get_bbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        h_ratio = (height / text_height)
        bbox_ratio = (width / text_width) * (height / text_height)
        font_size = round(self.size / bbox_ratio)
        new_text_bbox = self.get_bbox((0, 0), text, font_size)    
        new_text_width = new_text_bbox[2] - new_text_bbox[0]
        chars_in_line = math.ceil(new_text_width / width)

        new_text = "\n".join(wrap(text, chars_in_line))

        return new_text, font_size


if __name__ == "__main__":
    font = Font("static/fonts/BryndanWriteBook.ttf")
    image = Image.new("RGBA", (1000, 1000), "black")
    draw = ImageDraw.Draw(image)
    #text = "\n".join(wrap("TEST TESTTEST", 8))
    start = 100, 100    
    bbox = (*start, 500, 500)
    text = "Some random text to write :P"
    text, font_size = font.fit_in_bbox(bbox, text)
    print(text, font_size)
    draw.text(start, text, fill="white", font=font.get_font(font_size))
    draw.rectangle(bbox, outline="red")
    #bbox = font.get_bbox(start, text)
    print(bbox)
    #draw.rectangle(bbox, outline="red")
    print(bbox)
    print(font.get_size(text))
    image.show()
