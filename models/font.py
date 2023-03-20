from pathlib import Path


DEFAULT_PATH = Path("static") / "fonts"


class Font:
    variant_1: Path = DEFAULT_PATH / "BryndanWriteBook.ttf"
    variant_2: Path = DEFAULT_PATH / "Adigiana.ttf"
    variant_3: Path = DEFAULT_PATH / "carnetdevoyage.ttf"
    variant_4: Path = DEFAULT_PATH / "bainsley-bold1.otf"
    variant_5: Path = DEFAULT_PATH / "flow-bold1.otf"

    @classmethod
    def get_all(cls):
        _dict = cls.__dict__
        return [_dict[key] for key in _dict if key.startswith("variant")]
