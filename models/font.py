from dataclasses import dataclass

from textwrap import wrap
from PIL import ImageFont, Image, ImageDraw


@dataclass
class Font:
    path: str
    size: int

    def get_font(self, size=None):
        if size is None:
            return ImageFont.truetype(self.path, self.size)
        return ImageFont.truetype(self.path, size)

    def get_bbox(self, start, text):
        image = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox(start, text=text, font=self.get_font())
        return bbox

    def get_size(self, text):
        bbox = self.get_bbox((0, 0), text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def fit_in_bbox(self):
        pass
    

if __name__ == "__main__":
    font = Font("static/fonts/BryndanWriteBook.ttf", 100)
    image = Image.new("RGBA", (1000, 1000), "black")
    draw = ImageDraw.Draw(image)
    text = "\n".join(wrap("TEST TEST TEST", 5))
    start = 100, 100
    draw.text(start, text, fill="white", font=font.get_font())
    bbox = font.get_bbox(start, text)
    draw.rectangle(bbox, outline="red")
    print(bbox)
    print(font.get_size(text))
    image.show()
