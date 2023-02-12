from pathlib import Path


DEFAULT_PATH = Path("static") / "fonts"


class Font:
    variant_1: Path = DEFAULT_PATH / "BryndanWriteBook.ttf"
    variant_2: Path = DEFAULT_PATH / "Adigiana.ttf"
    