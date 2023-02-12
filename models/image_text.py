from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from models.palette import Palette


SYMBOL_LIMIT = 1000
TITLE_SYMBOL_LIMIT = 69


# TODO: refactor this class
# TODO: document this class
# TODO: add types
# TODO: integrate with PIL Image class (paste text on PIL Image)

class ImageText:
    def __init__(self, size: tuple[int, int], font_path: Path, palette: Palette):
        self.size = size
        self.font_path = str(font_path)
        self.palette = palette
        self.image = Image.new('RGBA', self.size, color=(0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def write_title(
        self, 
        pos, 
        text, 
        max_width=None, 
        max_height=None
    ):
        if len(text) >= TITLE_SYMBOL_LIMIT:
            return False
        return self._write_text(
            pos, text, None, None, max_width, max_height
        )

    def write_additional_text(
        self,
        pos, 
        text, 
        box_width,
        font_size=11, 
        place='center'
    ):
        if len(text) >= SYMBOL_LIMIT:
            return False
        return self._write_text_in_box(
            pos, text, box_width, font_size, place
        )

    def _get_text_size(self, font_size, text):
        font = ImageFont.truetype(self.font_path, font_size)
        return font.getsize(text)

    def _get_font_size(self, text, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self._get_text_size(font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError(f"Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self._get_text_size(font_size, text)

    def _write_text(self, pos, text, font_size=None, color=None, 
                    max_width=None, max_height=None):
        if color is None:
            color = self.palette.accent_color
        
        if font_size is None and (max_width is not None or max_height is not None):
            font_size = self._get_font_size(text, max_width, max_height)
        text_size = self._get_text_size(font_size, text)
        
        x, y = pos
        if x is None:
            x = (self.size[0] - text_size[0]) / 2
        if y is None:
            y = (self.size[1] - text_size[1]) / 2
            
        font = ImageFont.truetype(self.font_path, font_size)
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def _write_text_in_box(self, pos, text, box_width,
                       font_size=11, place='left'):
        color = self.palette.additional_color
        x, y = pos
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self._get_text_size(font_size, new_line)
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

        # TODO: add box_height somehow
        for line in lines:
            height += text_height
            if place == 'left':
                self._write_text((x, height), line, font_size, color)
            elif place == 'right':
                total_size = self._get_text_size(font_size, line)
                x_left = x + box_width - total_size[0]
                self._write_text((x_left, height), line, font_size, color)
            elif place == 'center':
                total_size = self._get_text_size(font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self._write_text((x_left, height), line, font_size, color)
        return (box_width, height - y)