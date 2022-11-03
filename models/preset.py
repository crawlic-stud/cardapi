from .palette import Palette


class Preset:
    """Premade color's presets."""
    
    # one primary color presets
    BLUE = Palette("#3a9cc5", "#08e6ed", "#e5fdff")
    GREEN = Palette("#246369", "#68e188", "#9affb5")
    RED = Palette("#c12600", "#ff6c05", "#ff5656")
    ORANGE = Palette("#ffa656", "#ff6600", "#ffd084")
    YELLOW = Palette("#fadc31", "#fffcc4", "#fff682")
    PINK = Palette("#fe66f0", "#ffbefa", "#fda1e1")
    PURPLE = Palette("#292359", "#cb33b2", "#9440c1")
    CYAN = Palette("#38646b", "#16b199", "#3be0c3")

    # multicolor presets
    NEON = Palette((255, 38, 143), (182, 148, 255), (83, 174, 252))
    LIME = Palette((31, 138, 15), (149, 255, 99), (240, 255, 33))
    DARK_SKY = Palette((22, 5, 51), (23, 26, 92), (71, 12, 33))
