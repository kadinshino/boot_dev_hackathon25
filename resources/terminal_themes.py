from enum import Enum
from typing import Dict, Tuple

class Theme(Enum):
    WHITE_BOOT = "white_boot"
    MATRIX_BLUE = "matrix_blue"
    CYBER_RED = "cyber_red"
    GLITCH_MODE = "glitch"
    AWAKENING = "awakening"

class ThemeColors:
    """Color palettes for each theme."""
    
    WHITE_BOOT = {
        'bg': (245, 245, 245),
        'text': (20, 20, 20),
        'terminal_bg': (255, 255, 255, 230),
        'terminal_border': (180, 180, 180),
        'terminal_text': (0, 0, 0),
        'stream_primary': (220, 220, 220),
        'stream_secondary': (180, 180, 180)
    }
    
    MATRIX_BLUE = {
        'bg': (0, 0, 0),
        'text': (100, 200, 255),
        'terminal_bg': (10, 15, 25, 180),
        'terminal_border': (80, 150, 220),
        'terminal_text': (150, 220, 255),
        'stream_primary': (100, 200, 255),
        'stream_secondary': (50, 120, 180)
    }
    
    CYBER_RED = {
        'bg': (15, 0, 0),
        'text': (255, 68, 68),
        'terminal_bg': (30, 10, 10, 200),
        'terminal_border': (200, 50, 50),
        'terminal_text': (255, 100, 100),
        'stream_primary': (255, 68, 68),
        'stream_secondary': (180, 40, 40)
    }
    
    @classmethod
    def get_palette(cls, theme: Theme) -> Dict[str, Tuple[int, ...]]:
        """Get color palette for a specific theme."""
        palettes = {
            Theme.WHITE_BOOT: cls.WHITE_BOOT,
            Theme.MATRIX_BLUE: cls.MATRIX_BLUE,
            Theme.CYBER_RED: cls.CYBER_RED,
        }
        return palettes.get(theme, cls.MATRIX_BLUE)