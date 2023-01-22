from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from models.palette import Palette


class ImageText():
    def __init__(self, size: tuple[int, int], font_path: str, palette: Palette):
        self.size = size
        self.font_path = font_path
        self.palette = palette
        self.background = Image.new('RGBA', self.size, color=(0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.background)
    
    def get_font_size(self, text, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError(f"Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font_size, text)

    def write_text(self, pos, text, color=(0, 0, 0), 
                    font_size=None, max_width=None, max_height=None):
        if font_size is None and (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, max_width, max_height)
        text_size = self.get_text_size(font_size, text)
        
        if pos is None:
            x = (self.size[0] - text_size[0]) / 2
            y = (self.size[1] - text_size[1]) / 2
        else:
            x, y = pos
            
        font = ImageFont.truetype(self.font_path, font_size)
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_size, text):
        font = ImageFont.truetype(self.font_path, font_size)
        return font.getsize(text)

    def write_text_box(self, pos, text, box_width,
                       font_size=11, color=(0, 0, 0), place='left'):
        x, y = pos
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_size, new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        height = y
        for line in lines:
            height += text_height
            if place == 'left':
                self.write_text((x, height), line, font_size, color)
            elif place == 'right':
                total_size = self.get_text_size(font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text((x_left, height), line,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text((x_left, height), line, font_size, color)
        return (box_width, height - y)