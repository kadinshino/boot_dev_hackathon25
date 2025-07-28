"""
Matrix rain effect component for The Basilisk Protocol.

This module handles the iconic falling character effect in the background.
"""

import random
import pygame
from typing import List
from dataclasses import dataclass

from config import MatrixConfig, Colors, FontConfig


@dataclass
class MatrixCharacter:
    """Represents a single character in a matrix stream."""
    y: float
    char: str
    age: int


class MatrixStream:
    """
    Manages a single vertical stream of falling characters.
    
    Each stream has its own speed and spawn rate, creating
    a varied and organic-looking effect.
    """
    
    def __init__(self, x: int) -> None:
        """
        Initialize a matrix stream at the given x coordinate.
        
        Args:
            x: The horizontal position of this stream
        """
        self.x = x
        self.characters: List[MatrixCharacter] = []
        self.speed = random.randint(MatrixConfig.MIN_SPEED, MatrixConfig.MAX_SPEED)
        self.spawn_chance = random.uniform(
            MatrixConfig.MIN_SPAWN_CHANCE, 
            MatrixConfig.MAX_SPAWN_CHANCE
        )
    
    def update(self) -> None:
        """Update the stream's characters for one frame."""
        self._spawn_new_character()
        self._update_existing_characters()
        self._remove_old_characters()
    
    def _spawn_new_character(self) -> None:
        """Attempt to spawn a new character at the top of the stream."""
        can_spawn = (
            random.random() < self.spawn_chance and 
            len(self.characters) < MatrixConfig.MAX_CHARS_PER_STREAM
        )
        
        if can_spawn:
            new_char = MatrixCharacter(
                y=-FontConfig.STREAM_FONT_SIZE,
                char=random.choice(MatrixConfig.CHARACTER_SET),
                age=0
            )
            self.characters.append(new_char)
    
    def _update_existing_characters(self) -> None:
        """Update position and appearance of existing characters."""
        for char in self.characters:
            # Move character down
            char.y += self.speed
            char.age += 1
            
            # Occasionally change the character for flicker effect
            if random.random() < MatrixConfig.FLICKER_CHANCE:
                char.char = random.choice(MatrixConfig.CHARACTER_SET)
    
    def _remove_old_characters(self) -> None:
        """Remove characters that have moved off screen."""
        screen_bottom = pygame.display.get_surface().get_height()
        max_y = screen_bottom + FontConfig.STREAM_FONT_SIZE
        self.characters = [char for char in self.characters if char.y < max_y]
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Draw all visible characters in the stream.
        
        Args:
            surface: The surface to draw on
            font: The font to use for rendering characters
        """
        for i, char in enumerate(self.characters):
            if self._is_character_visible(char, surface.get_height()):
                color, alpha = self._get_character_appearance(i)
                text = font.render(char.char, True, color)
                text.set_alpha(alpha)
                surface.blit(text, (self.x, char.y))
    
    def _is_character_visible(self, char: MatrixCharacter, screen_height: int) -> bool:
        """Check if a character is within the visible screen area."""
        return 0 <= char.y < screen_height
    
    def _get_character_appearance(self, index: int) -> tuple:
        """
        Calculate color and alpha for a character based on its position.
        
        Args:
            index: The character's position in the stream
            
        Returns:
            Tuple of (color, alpha) values
        """
        # Head of stream is brightest
        if index == 0:
            return Colors.ICE_BLUE, 255
        
        # Calculate fade based on position
        fade_factor = max(0, 1 - (index / MatrixConfig.FADE_LENGTH))
        alpha = int(255 * fade_factor)
        
        # Bright characters near head, darker ones trailing
        color = (Colors.ICE_BLUE if index <= MatrixConfig.BRIGHT_HEAD_COUNT 
                else Colors.DARK_ICE_BLUE)
        
        return color, alpha
    
    def clear(self) -> None:
        """Clear all characters from this stream."""
        self.characters.clear()


class MatrixRainEffect:
    """
    Manages the complete matrix rain effect across the screen.
    
    Creates and manages multiple streams to fill the display with
    falling characters.
    """
    
    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the matrix rain effect.
        
        Args:
            screen_width: Width of the display area
            screen_height: Height of the display area
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._initialize_streams()
    
    def _initialize_streams(self) -> None:
        """Create streams across the width of the screen."""
        stream_spacing = FontConfig.STREAM_FONT_SIZE
        self.streams = [
            MatrixStream(x) 
            for x in range(0, self.screen_width, stream_spacing)
        ]
    
    def update(self) -> None:
        """Update all streams for one frame."""
        for stream in self.streams:
            stream.update()
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Draw all streams to the given surface.
        
        Args:
            surface: The surface to draw on
            font: The font to use for rendering
        """
        for stream in self.streams:
            stream.draw(surface, font)
    
    def clear_all_streams(self) -> None:
        """Clear all characters from all streams."""
        for stream in self.streams:
            stream.clear()
    
    def set_intensity(self, intensity: float) -> None:
        """
        Adjust the intensity of the effect.
        
        Args:
            intensity: Value between 0.0 and 1.0
        """
        intensity = max(0.0, min(1.0, intensity))
        
        for stream in self.streams:
            # Adjust spawn chance based on intensity
            base_chance = random.uniform(
                MatrixConfig.MIN_SPAWN_CHANCE,
                MatrixConfig.MAX_SPAWN_CHANCE
            )
            stream.spawn_chance = base_chance * intensity
