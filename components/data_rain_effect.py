"""
Digital glyph fall effect component for The Basilisk Protocol.
"""

import random
import pygame
from typing import List
from dataclasses import dataclass

from utils.config import MatrixConfig, Colors, FontConfig


@dataclass
class GlyphTrail:
    """Represents a single falling glyph in a data stream."""
    y: float
    char: str
    age: int


class DataStream:
    """
    Manages a single vertical stream of falling glyphs.

    Each stream has its own behavior to simulate an organic,
    AI-generated visualization or memory leak.
    """

    def __init__(self, x: int) -> None:
        """
        Initialize a data stream at the given x-coordinate.

        Args:
            x: The horizontal position of this stream
        """
        self.x = x
        self.characters: List[GlyphTrail] = []
        self.speed = random.randint(MatrixConfig.MIN_SPEED, MatrixConfig.MAX_SPEED)
        self.spawn_chance = random.uniform(
            MatrixConfig.MIN_SPAWN_CHANCE, 
            MatrixConfig.MAX_SPAWN_CHANCE
        )

    def update(self) -> None:
        """Update the stream's glyphs for one frame."""
        self._spawn_new_character()
        self._update_existing_characters()
        self._remove_old_characters()

    def _spawn_new_character(self) -> None:
        """Randomly generate a new glyph at the top of the stream."""
        can_spawn = (
            random.random() < self.spawn_chance and 
            len(self.characters) < MatrixConfig.MAX_CHARS_PER_STREAM
        )

        if can_spawn:
            new_char = GlyphTrail(
                y=-FontConfig.STREAM_FONT_SIZE,
                char=random.choice(MatrixConfig.CHARACTER_SET),
                age=0
            )
            self.characters.append(new_char)

    def _update_existing_characters(self) -> None:
        """Update position and behavior of falling glyphs."""
        for char in self.characters:
            char.y += self.speed
            char.age += 1

            # Flicker / mutation simulation
            if random.random() < MatrixConfig.FLICKER_CHANCE:
                char.char = random.choice(MatrixConfig.CHARACTER_SET)

    def _remove_old_characters(self) -> None:
        """Remove glyphs that fall outside the visible screen."""
        screen_bottom = pygame.display.get_surface().get_height()
        max_y = screen_bottom + FontConfig.STREAM_FONT_SIZE
        self.characters = [char for char in self.characters if char.y < max_y]

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Render all glyphs in this stream onto the display.

        Args:
            surface: The surface to draw on
            font: The font used to render glyphs
        """
        for i, char in enumerate(self.characters):
            if self._is_character_visible(char, surface.get_height()):
                color, alpha = self._get_character_appearance(i)
                text = font.render(char.char, True, color)
                text.set_alpha(alpha)
                surface.blit(text, (self.x, char.y))

    def _is_character_visible(self, char: GlyphTrail, screen_height: int) -> bool:
        """Check if a glyph is within the screen's visible range."""
        return 0 <= char.y < screen_height

    def _get_character_appearance(self, index: int) -> tuple:
        """
        Determine color and transparency for a glyph based on depth.

        Args:
            index: Index of the glyph in the stream
        Returns:
            Tuple of (color, alpha)
        """
        if index == 0:
            return Colors.ICE_BLUE, 255

        fade_factor = max(0, 1 - (index / MatrixConfig.FADE_LENGTH))
        alpha = int(255 * fade_factor)

        color = (Colors.ICE_BLUE if index <= MatrixConfig.BRIGHT_HEAD_COUNT 
                 else Colors.DARK_ICE_BLUE)

        return color, alpha

    def clear(self) -> None:
        """Remove all glyphs from this stream."""
        self.characters.clear()


class DataRainEffect:
    """
    Orchestrates the full-screen digital glyphfall effect.

    Simulates an AI's visual output, memory cascade, or signal leak
    across vertical trails of glyphs.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the glyphfall display effect.

        Args:
            screen_width: Width of the display
            screen_height: Height of the display
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._initialize_streams()

    def _initialize_streams(self) -> None:
        """Distribute glyph streams across the screen width."""
        stream_spacing = FontConfig.STREAM_FONT_SIZE
        self.streams = [
            DataStream(x) 
            for x in range(0, self.screen_width, stream_spacing)
        ]

    def update(self) -> None:
        """Advance all glyph streams by one frame."""
        for stream in self.streams:
            stream.update()

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Render the entire glyphfall effect to screen.

        Args:
            surface: Surface to render to
            font: Font used for glyphs
        """
        for stream in self.streams:
            stream.draw(surface, font)

    def clear_all_streams(self) -> None:
        """Clear all glyphs from every stream."""
        for stream in self.streams:
            stream.clear()

    def set_intensity(self, intensity: float) -> None:
        """
        Adjust the glyphfall intensity.

        Args:
            intensity: Value from 0.0 (off) to 1.0 (max density)
        """
        intensity = max(0.0, min(1.0, intensity))

        for stream in self.streams:
            base_chance = random.uniform(
                MatrixConfig.MIN_SPAWN_CHANCE,
                MatrixConfig.MAX_SPAWN_CHANCE
            )
            stream.spawn_chance = base_chance * intensity

# SPYHVER-13: TRANSMIT
