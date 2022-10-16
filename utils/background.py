import random

from PIL import Image, ImageFilter, ImageDraw


def create_simple_background(color1, color2):
    bg = Image.new("RGBA", (1000, 1000), color2)
    draw = ImageDraw.Draw(bg)
    for _ in range(25):
        color = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
        center_x = random.randint(0, 1000)
        center_y = random.randint(0, 1000)
        radius = 75
        draw.ellipse((center_x-radius, center_y-radius, center_x+radius, center_y+radius), fill=color)
    
    draw.ellipse((250, 250, 750, 750), fill=(200, 200, 10))
    bg = bg.filter(ImageFilter.BoxBlur(250))
    bg.show()


if __name__ == "__main__":
    create_simple_background((10, 30, 100), (100, 100, 255))
