"""
Title screen component for The Basilisk Protocol.

Manages the initial title screen display, boot sequence animation,
and transition to the main game.
"""

import pygame
import random
import math
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from config import (
    TitleScreenConfig,
    Colors,
    MatrixConfig,
    TerminalConfig,
    TITLE_MESSAGES,
    BOOT_SEQUENCE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

@dataclass
class TitleScreenState:
    """Encapsulates the state of the title screen."""
    # Fields without defaults would go here (but we don't have any)
    
    # Fields with defaults
    active: bool = True
    pulse_phase: float = 0.0
    current_message_index: int = 0
    message_timer: int = 0
    input_text: str = ""
    cursor_visible: bool = True
    cursor_timer: int = 0
    glitch_active: bool = False
    glitch_timer: int = 0
    boot_sequence_active: bool = False
    boot_sequence_index: int = 0
    boot_sequence_timer: int = 0
    debug_mode_requested: bool = False
    boot_lines: List[str] = field(default_factory=list)  # This must come last

class TitleScreen:
    """
    Manages the title screen experience.
    
    Handles the animated title display, user input prompt,
    and boot sequence animation when the correct command is entered.
    """
    
    def __init__(self, screen: pygame.Surface, fonts: Dict[str, pygame.font.Font]) -> None:
        """
        Initialize the title screen.
        
        Args:
            screen: The pygame surface to draw on
            fonts: Dictionary of fonts for different text elements
        """
        self.screen = screen
        self.fonts = fonts
        self.state = TitleScreenState()
        
        # Pre-calculate some values for efficiency
        self.screen_center_x = SCREEN_WIDTH // 2
        self.screen_center_y = SCREEN_HEIGHT // 2
        self.title_y = SCREEN_HEIGHT // 3
        self.mini_terminal_y = SCREEN_HEIGHT * 2 // 3
    
    def update(self) -> bool:
        """
        Update title screen animations and state.
        
        Returns:
            True if the boot sequence is complete and game should start
        """
        if self.state.boot_sequence_active:
            return self._update_boot_sequence()
        else:
            self._update_idle_animations()
            return False
    
    def _update_idle_animations(self) -> None:
        """Update animations for the idle title screen."""
        # Update pulse effect
        self.state.pulse_phase += TitleScreenConfig.PULSE_SPEED
        
        # Update cursor blink
        self.state.cursor_timer += 1
        if self.state.cursor_timer > TerminalConfig.CURSOR_BLINK_RATE:
            self.state.cursor_visible = not self.state.cursor_visible
            self.state.cursor_timer = 0
        
        # Update message cycling
        self.state.message_timer += 1
        if self.state.message_timer > TitleScreenConfig.MESSAGE_CYCLE_TIME:
            self.state.message_timer = 0
            self.state.current_message_index = (
                (self.state.current_message_index + 1) % len(TITLE_MESSAGES)
            )
        
        # Random glitch effect
        self._update_glitch_effect()
    
    def _update_glitch_effect(self) -> None:
        """Update the random glitch effect."""
        if random.random() < TitleScreenConfig.GLITCH_CHANCE:
            self.state.glitch_active = True
            self.state.glitch_timer = random.randint(3, 8)
        
        if self.state.glitch_timer > 0:
            self.state.glitch_timer -= 1
            if self.state.glitch_timer == 0:
                self.state.glitch_active = False
    
    def _update_boot_sequence(self) -> bool:
        """
        Update the boot sequence animation.
        
        Returns:
            True if boot sequence is complete
        """
        self.state.boot_sequence_timer += 1
        
        if self.state.boot_sequence_timer > TitleScreenConfig.BOOT_LINE_DELAY:
            self.state.boot_sequence_timer = 0
            
            if self.state.boot_sequence_index < len(BOOT_SEQUENCE):
                # Add next line
                self.state.boot_lines.append(BOOT_SEQUENCE[self.state.boot_sequence_index])
                self.state.boot_sequence_index += 1
            else:
                # Boot sequence complete
                self.state.boot_sequence_active = False
                return True
        
        return False
    
    def handle_input(self, char: str) -> None:
        """
        Handle character input.
        
        Args:
            char: The character typed by the user
        """
        if len(self.state.input_text) < 20:  # Limit input length
            self.state.input_text += char
    
    def handle_backspace(self) -> None:
        """Handle backspace key press."""
        self.state.input_text = self.state.input_text[:-1]
    
    def handle_enter(self) -> bool:
        """
        Handle enter key press.
        
        Returns:
            True if the boot sequence should start or skip to terminal
        """
        command = self.state.input_text.lower().strip()
        
        if command == "boot.dev":
            self.state.boot_sequence_active = True
            return False  # Don't transition yet, show boot sequence first
        elif command == "boot.debug":
            # Skip boot sequence and go straight to terminal for debug mode
            self.state.debug_mode_requested = True
            return True  # Immediately transition to terminal
        
        # Clear input if wrong command
        self.state.input_text = ""
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the title screen.
        
        Args:
            surface: The surface to draw on
        """
        if self.state.boot_sequence_active:
            self._draw_boot_sequence(surface)
        else:
            self._draw_idle_screen(surface)
    
    def _draw_idle_screen(self, surface: pygame.Surface) -> None:
        """Draw the main title screen in idle state."""
        # Draw glowing title
        self._draw_glowing_title(surface)
        
        # Draw cycling message
        self._draw_cycling_message(surface)
        
        # Draw mini terminal
        self._draw_mini_terminal(surface)
    
    def _draw_glowing_title(self, surface: pygame.Surface) -> None:
        """Draw the title with glow effect."""
        # Calculate pulse intensity
        pulse_intensity = (math.sin(self.state.pulse_phase) + 1) / 2
        glow_alpha = int(100 + 155 * pulse_intensity)
        
        # Get title text (with optional glitch)
        title_text = self._get_title_text()
        
        # Render title
        title_font = self.fonts['title']
        title_surface = title_font.render(title_text, True, Colors.TITLE_CORE)
        title_rect = title_surface.get_rect(center=(self.screen_center_x, self.title_y))
        
        # Draw glow layers
        self._draw_glow_layers(surface, title_text, title_rect, glow_alpha)
        
        # Draw main title
        surface.blit(title_surface, title_rect)
    
    def _get_title_text(self) -> str:
        """Get the title text, applying glitch effect if active."""
        title_text = "BASILISK_PROTOCOL"
        
        if self.state.glitch_active:
            # Apply glitch effect
            title_text = ''.join(
                random.choice(MatrixConfig.CHARACTER_SET) if random.random() < 0.3 else c 
                for c in title_text
            )
        
        return title_text
    
    def _draw_glow_layers(
        self, 
        surface: pygame.Surface, 
        text: str, 
        base_rect: pygame.Rect, 
        alpha: int
    ) -> None:
        """Draw multiple glow layers for text effect."""
        title_font = self.fonts['title']
        
        for i in range(3, 0, -1):
            glow_surface = title_font.render(text, True, Colors.TITLE_GLOW)
            glow_surface.set_alpha(alpha // i)
            
            # Add glitch offset if active
            offset_x = random.randint(-2, 2) if self.state.glitch_active else 0
            offset_y = random.randint(-2, 2) if self.state.glitch_active else 0
            
            glow_rect = glow_surface.get_rect(
                center=(base_rect.centerx + offset_x, base_rect.centery + offset_y)
            )
            
            # Scale up for glow effect
            scale_factor = 1 + i * 0.05
            glow_surface = pygame.transform.scale(
                glow_surface,
                (int(glow_rect.width * scale_factor), 
                 int(glow_rect.height * scale_factor))
            )
            glow_rect = glow_surface.get_rect(center=glow_rect.center)
            
            surface.blit(glow_surface, glow_rect)
    
    def _draw_cycling_message(self, surface: pygame.Surface) -> None:
        """Draw the cycling status message."""
        message = TITLE_MESSAGES[self.state.current_message_index]
        message_font = self.fonts['subtitle']
        message_surface = message_font.render(message, True, Colors.TERMINAL_TEXT)
        message_rect = message_surface.get_rect(
            center=(self.screen_center_x, self.screen_center_y)
        )
        message_surface.set_alpha(200)
        surface.blit(message_surface, message_rect)
    
    def _draw_mini_terminal(self, surface: pygame.Surface) -> None:
        """Draw the mini terminal input box."""
        width = TitleScreenConfig.MINI_TERMINAL_WIDTH
        height = TitleScreenConfig.MINI_TERMINAL_HEIGHT
        x = (SCREEN_WIDTH - width) // 2
        y = self.mini_terminal_y
        
        # Create terminal surface
        terminal_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        terminal_surface.fill((10, 15, 25, 200))
        
        # Draw border
        pygame.draw.rect(
            terminal_surface, 
            Colors.TERMINAL_BORDER, 
            (0, 0, width, height), 
            2
        )
        
        # Draw input text
        font = self.fonts['mini_terminal']
        cursor = "_" if self.state.cursor_visible else ""
        input_line = f"> {self.state.input_text}{cursor}"
        text_surface = font.render(input_line, True, Colors.TERMINAL_TEXT)
        text_y = (height - text_surface.get_height()) // 2
        terminal_surface.blit(text_surface, (10, text_y))
        
        # Draw hint if input is empty
        if not self.state.input_text:
            hint_text = "Type 'boot.dev' to begin..."
            hint_surface = font.render(hint_text, True, Colors.DARK_ICE_BLUE)
            hint_surface.set_alpha(100)
            hint_x = width - hint_surface.get_width() - 30
            terminal_surface.blit(hint_surface, (hint_x, text_y))
        
        surface.blit(terminal_surface, (x, y))
    
    def _draw_boot_sequence(self, surface: pygame.Surface) -> None:
        """Draw the boot sequence animation."""
        # Dark background
        surface.fill(Colors.BLACK)
        
        # Draw boot lines
        font = self.fonts['terminal']
        y_offset = 50
        line_height = 25
        
        for i, line in enumerate(self.state.boot_lines):
            # Determine line color
            color = self._get_boot_line_color(line)
            
            # Render line
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (50, y_offset + i * line_height))
        
        # Add blinking cursor at the end
        if self.state.cursor_visible and len(self.state.boot_lines) < len(BOOT_SEQUENCE):
            cursor_y = y_offset + len(self.state.boot_lines) * line_height
            cursor_surface = font.render("_", True, Colors.TERMINAL_TEXT)
            surface.blit(cursor_surface, (50, cursor_y))
    
    def _get_boot_line_color(self, line: str) -> tuple:
        """Get the appropriate color for a boot sequence line."""
        if "WARNING" in line:
            return Colors.WARNING_RED
        elif "[OK]" in line:
            return Colors.SUCCESS_GREEN
        elif "BASILISK" in line or "OMEGA" in line:
            return Colors.ICE_BLUE
        else:
            return Colors.TERMINAL_TEXT

# SPYHVER-15: FRACTURED
