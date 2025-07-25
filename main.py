# =============================================================================
############################ Terminal Game Concept ############################
# =============================================================================

# import pygame
#!/usr/bin/env python3

import pygame
import random
import asyncio
import platform
import string
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# CONSTANTS
# =============================================================================

# Screen Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Hackathon 25"
TARGET_FPS = 60

# Colors (RGB tuples)
class Colors:
    ICE_BLUE = (100, 200, 255)
    DARK_ICE_BLUE = (50, 120, 180)
    BLACK = (0, 0, 0)
    TERMINAL_BG = (10, 15, 25, 180)  # RGBA with alpha
    TERMINAL_BORDER = (80, 150, 220)
    TERMINAL_TEXT = (150, 220, 255)

# Font Configuration
class FontConfig:
    STREAM_FONT_NAME = "courier"
    STREAM_FONT_SIZE = 20
    TERMINAL_FONT_NAME = "consolas"
    TERMINAL_FONT_SIZE = 16

# Stream Configuration
class StreamConfig:
    MIN_SPEED = 1
    MAX_SPEED = 4
    MIN_SPAWN_CHANCE = 0.02
    MAX_SPAWN_CHANCE = 0.08
    MAX_CHARS_PER_STREAM = 30
    FLICKER_CHANCE = 0.03
    FADE_LENGTH = 15
    BRIGHT_HEAD_COUNT = 3

# Terminal Configuration
class TerminalConfig:
    # Default terminal size (50% of screen)
    WIDTH_RATIO = 0.5
    HEIGHT_RATIO = 0.5
    X_OFFSET_RATIO = 0.25
    Y_OFFSET_RATIO = 0.25
    
    # Expanded terminal size (95% of screen)
    EXPANDED_WIDTH_RATIO = 0.95
    EXPANDED_HEIGHT_RATIO = 0.95
    EXPANDED_X_OFFSET_RATIO = 0.025
    EXPANDED_Y_OFFSET_RATIO = 0.025
    
    BORDER_WIDTH = 2
    TITLE_BAR_HEIGHT = 25
    LINE_HEIGHT = 22
    TEXT_MARGIN = 10
    TITLE_MARGIN = 8
    TITLE_Y_OFFSET = 5
    CONTENT_Y_OFFSET = 35
    MAX_INPUT_LENGTH = 50
    CURSOR_BLINK_RATE = 30  # frames

# Character Sets
CHARACTER_SET = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Default Terminal Messages
DEFAULT_TERMINAL_LINES = [
    "> SYSTEM INITIALIZATION...",
    "> Loading neural networks...",
    "> Establishing connection...",
    "> Authentication successful",
    "> Access granted to mainframe",
    "> Downloading data streams...",
    "> Matrix protocols active",
    "> Awaiting user input...",
    "> Type 'start' to begin the game",
    ""
]


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Character:
    """Represents a single character in the matrix stream."""
    y: float
    char: str
    age: int


@dataclass
class TerminalState:
    """Holds the current state of the terminal."""
    lines: List[str]
    current_input: str
    cursor_visible: bool
    cursor_timer: int
    expanded: bool = False


# =============================================================================
# CORE CLASSES
# =============================================================================

class MatrixStream:
    """Handles a single column of falling matrix characters."""
    
    def __init__(self, x: int) -> None:
        self.x = x
        self.characters: List[Character] = []
        self.speed = random.randint(StreamConfig.MIN_SPEED, StreamConfig.MAX_SPEED)
        self.spawn_chance = random.uniform(
            StreamConfig.MIN_SPAWN_CHANCE, 
            StreamConfig.MAX_SPAWN_CHANCE
        )
        
    def update(self) -> None:
        """Update stream positions and spawn new characters."""
        self._spawn_new_character()
        self._update_character_positions()
        self._apply_flicker_effect()
        self._remove_offscreen_characters()
    
    def _spawn_new_character(self) -> None:
        """Spawn a new character at the top of the stream."""
        if (random.random() < self.spawn_chance and 
            len(self.characters) < StreamConfig.MAX_CHARS_PER_STREAM):
            
            new_char = Character(
                y=-FontConfig.STREAM_FONT_SIZE,
                char=random.choice(CHARACTER_SET),
                age=0
            )
            self.characters.append(new_char)
    
    def _update_character_positions(self) -> None:
        """Update positions and ages of all characters."""
        for char in self.characters:
            char.y += self.speed
            char.age += 1
    
    def _apply_flicker_effect(self) -> None:
        """Randomly change characters for flickering effect."""
        for char in self.characters:
            if random.random() < StreamConfig.FLICKER_CHANCE:
                char.char = random.choice(CHARACTER_SET)
    
    def _remove_offscreen_characters(self) -> None:
        """Remove characters that have moved off screen."""
        self.characters = [
            char for char in self.characters 
            if char.y < SCREEN_HEIGHT + FontConfig.STREAM_FONT_SIZE
        ]
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Render the stream to the given surface."""
        for i, char in enumerate(self.characters):
            if 0 <= char.y < SCREEN_HEIGHT:
                color, alpha = self._get_character_appearance(i)
                text = font.render(char.char, True, color)
                text.set_alpha(alpha)
                surface.blit(text, (self.x, char.y))
    
    def _get_character_appearance(self, index: int) -> Tuple[Tuple[int, int, int], int]:
        """Calculate color and alpha for character based on position in stream."""
        if index == 0:  # Head of stream
            return Colors.ICE_BLUE, 255
        
        fade_factor = max(0, 1 - (index / StreamConfig.FADE_LENGTH))
        alpha = int(255 * fade_factor)
        color = Colors.ICE_BLUE if index <= StreamConfig.BRIGHT_HEAD_COUNT else Colors.DARK_ICE_BLUE
        
        return color, alpha


class Terminal:
    """Handles the interactive terminal overlay."""
    
    def __init__(self) -> None:
        self.state = TerminalState(
            lines=DEFAULT_TERMINAL_LINES.copy(),
            current_input="",
            cursor_visible=True,
            cursor_timer=0,
            expanded=False
        )
        
        # Calculate initial terminal dimensions
        self._update_dimensions()
    
    def _update_dimensions(self) -> None:
        """Update terminal dimensions based on expanded state."""
        if self.state.expanded:
            self.width = int(SCREEN_WIDTH * TerminalConfig.EXPANDED_WIDTH_RATIO)
            self.height = int(SCREEN_HEIGHT * TerminalConfig.EXPANDED_HEIGHT_RATIO)
            self.x = int(SCREEN_WIDTH * TerminalConfig.EXPANDED_X_OFFSET_RATIO)
            self.y = int(SCREEN_HEIGHT * TerminalConfig.EXPANDED_Y_OFFSET_RATIO)
        else:
            self.width = int(SCREEN_WIDTH * TerminalConfig.WIDTH_RATIO)
            self.height = int(SCREEN_HEIGHT * TerminalConfig.HEIGHT_RATIO)
            self.x = int(SCREEN_WIDTH * TerminalConfig.X_OFFSET_RATIO)
            self.y = int(SCREEN_HEIGHT * TerminalConfig.Y_OFFSET_RATIO)
    
    def expand(self) -> None:
        """Expand the terminal to 95% of screen size."""
        self.state.expanded = True
        self._update_dimensions()
    
    def collapse(self) -> None:
        """Collapse the terminal back to normal size."""
        self.state.expanded = False
        self._update_dimensions()
    
    def update(self) -> None:
        """Update terminal state (cursor blinking)."""
        self.state.cursor_timer += 1
        if self.state.cursor_timer > TerminalConfig.CURSOR_BLINK_RATE:
            self.state.cursor_visible = not self.state.cursor_visible
            self.state.cursor_timer = 0
    
    def handle_input(self, char: str) -> None:
        """Add a character to the current input."""
        if len(self.state.current_input) < TerminalConfig.MAX_INPUT_LENGTH:
            self.state.current_input += char
    
    def handle_backspace(self) -> None:
        """Remove the last character from input."""
        if self.state.current_input:
            self.state.current_input = self.state.current_input[:-1]

    """Basic Commands and logic"""

    def execute_command(self) -> None:
        """Execute the current command and clear input."""
        if self.state.current_input.strip():
            self._process_command(self.state.current_input)
            self.state.current_input = ""
    
    def _process_command(self, command: str) -> None:
        """Process and respond to terminal commands."""
        self.state.lines.append(f"> {command}")
        command_lower = command.lower().strip()
        
        command_handlers = {
            "help": self._handle_help,
            "clear": self._handle_clear,
            "status": self._handle_status,
            "matrix": self._handle_matrix,
            "exit": self._handle_exit,
            "hello": self._handle_greeting,
            "hi": self._handle_greeting,
            "start": self._handle_start,
            "stop": self._handle_stop,
            "minimize": self._handle_minimize,
        }
        
        handler = command_handlers.get(command_lower, self._handle_unknown)
        handler(command)
    
    def _handle_help(self, command: str) -> None:
        """Show available commands."""
        help_lines = [
            "Available commands:",
            "  help - Show this help",
            "  clear - Clear terminal",
            "  status - System status",
            "  matrix - Matrix info",
            "  start - Begin game (expand terminal)",
            "  stop/minimize - Return to normal view",
            "  exit - Close terminal"
        ]
        self.state.lines.extend(help_lines)
    
    def _handle_clear(self, command: str) -> None:
        """Clear the terminal."""
        self.state.lines = ["Terminal cleared.", ""]
    
    def _handle_status(self, command: str) -> None:
        """Show system status."""
        status_info = [
            "System Status: ONLINE",
            f"Terminal Mode: {'EXPANDED' if self.state.expanded else 'NORMAL'}",
            f"Terminal Size: {self.width}x{self.height}",
            "Connections: 1,337 active",
            "Data streams: FLOWING",
            "Security: BREACH DETECTED"
        ]
        self.state.lines.extend(status_info)
    
    def _handle_matrix(self, command: str) -> None:
        """Show matrix information."""
        self.state.lines.extend([
            "Matrix Digital Rain v1.0",
            "Code streams: ACTIVE",
            "Reality.exe has stopped working",
            "Take the blue pill? [Y/N]"
        ])
    
    def _handle_start(self, command: str) -> None:
        """Handle start command - expand terminal for game mode."""
        if not self.state.expanded:
            self.expand()
            self.state.lines.extend([
                "GAME MODE ACTIVATED",
                "Terminal expanded to 95% view",
                "Welcome to the game area!",
                "Type 'stop' or 'minimize' to return to normal view",
                ""
            ])
        else:
            self.state.lines.append("Game mode already active!")
    
    def _handle_stop(self, command: str) -> None:
        """Handle stop command - return to normal terminal size."""
        if self.state.expanded:
            self.collapse()
            self.state.lines.extend([
                "GAME MODE DEACTIVATED",
                "Terminal returned to normal size",
                "Type 'start' to re-enter game mode",
                ""
            ])
        else:
            self.state.lines.append("Not in game mode!")
    
    def _handle_minimize(self, command: str) -> None:
        """Handle minimize command - same as stop."""
        self._handle_stop(command)
    
    def _handle_exit(self, command: str) -> None:
        """Handle exit command."""
        self.state.lines.append("Connection terminated.")
    
    def _handle_greeting(self, command: str) -> None:
        """Handle greeting commands."""
        self.state.lines.append("Greetings, user. Welcome to the Matrix.")
    
    def _handle_unknown(self, command: str) -> None:
        """Handle unknown commands."""
        self.state.lines.extend([
            f"Unknown command: '{command}'",
            "Type 'help' for available commands."
        ])
    
    """Visual Logic"""

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Render the terminal to the given surface."""
        terminal_surface = self._create_terminal_surface()
        self._draw_title_bar(terminal_surface, font)
        self._draw_content(terminal_surface, font)
        surface.blit(terminal_surface, (self.x, self.y))
    
    def _create_terminal_surface(self) -> pygame.Surface:
        """Create the terminal background surface."""
        terminal_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        terminal_surface.fill(Colors.TERMINAL_BG)
        pygame.draw.rect(
            terminal_surface, 
            Colors.TERMINAL_BORDER,
            (0, 0, self.width, self.height), 
            TerminalConfig.BORDER_WIDTH
        )
        return terminal_surface
    
    def _draw_title_bar(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal title bar."""
        pygame.draw.rect(
            surface, 
            Colors.TERMINAL_BORDER,
            (0, 0, self.width, TerminalConfig.TITLE_BAR_HEIGHT)
        )
        title_text = "TERMINAL v2.1"
        if self.state.expanded:
            title_text += " - GAME MODE"
        
        title_surface = font.render(title_text, True, Colors.BLACK)
        surface.blit(title_surface, (TerminalConfig.TITLE_MARGIN, TerminalConfig.TITLE_Y_OFFSET))
    
    def _draw_content(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal content lines."""
        display_lines = self._get_display_lines()
        max_lines = (self.height - TerminalConfig.CONTENT_Y_OFFSET) // TerminalConfig.LINE_HEIGHT
        visible_lines = display_lines[-max_lines:]
        
        for i, line in enumerate(visible_lines):
            y_pos = TerminalConfig.CONTENT_Y_OFFSET + i * TerminalConfig.LINE_HEIGHT
            text_surface = font.render(line, True, Colors.TERMINAL_TEXT)
            surface.blit(text_surface, (TerminalConfig.TEXT_MARGIN, y_pos))
    
    def _get_display_lines(self) -> List[str]:
        """Get all lines to display including current input."""
        lines = self.state.lines.copy()
        input_line = f"> {self.state.current_input}"
        if self.state.cursor_visible:
            input_line += "_"
        lines.append(input_line)
        return lines


class MatrixRainApp:
    """Main application class that orchestrates the matrix rain effect."""
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.stream_font = pygame.font.SysFont(
            FontConfig.STREAM_FONT_NAME, 
            FontConfig.STREAM_FONT_SIZE
        )
        self.terminal_font = pygame.font.SysFont(
            FontConfig.TERMINAL_FONT_NAME, 
            FontConfig.TERMINAL_FONT_SIZE
        )
        
        # Initialize streams and terminal
        self.streams = self._create_streams()
        self.terminal = Terminal()
        self.running = True
    
    def _create_streams(self) -> List[MatrixStream]:
        """Create matrix streams across the screen width."""
        return [
            MatrixStream(x) 
            for x in range(0, SCREEN_WIDTH, FontConfig.STREAM_FONT_SIZE)
        ]
    
    def handle_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
    
    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keyboard input events."""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_SPACE and pygame.key.get_pressed()[pygame.K_LCTRL]:
            self._reset_streams()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.terminal.execute_command()
        elif event.key == pygame.K_BACKSPACE:
            self.terminal.handle_backspace()
        elif event.unicode.isprintable():
            self.terminal.handle_input(event.unicode)
    
    def _reset_streams(self) -> None:
        """Clear all stream characters (Ctrl+Space shortcut)."""
        for stream in self.streams:
            stream.characters.clear()
    
    def update(self) -> None:
        """Update all game objects."""
        for stream in self.streams:
            stream.update()
        self.terminal.update()
    
    def draw(self) -> None:
        """Render the entire scene."""
        self.screen.fill(Colors.BLACK)
        
        # Draw matrix streams (only if terminal is not expanded, or draw them dimmed)
        if not self.terminal.state.expanded:
            for stream in self.streams:
                stream.draw(self.screen, self.stream_font)
        else:
            # Draw dimmed matrix streams in expanded mode
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_surface.fill(Colors.BLACK)
            for stream in self.streams:
                stream.draw(temp_surface, self.stream_font)
            temp_surface.set_alpha(50)  # Make streams very dim
            self.screen.blit(temp_surface, (0, 0))
        
        # Draw terminal overlay
        self.terminal.draw(self.screen, self.terminal_font)
        
        pygame.display.flip()
    
    async def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # Platform-specific frame rate control
            if platform.system() == "Emscripten":
                await asyncio.sleep(1.0 / TARGET_FPS)
            else:
                self.clock.tick(TARGET_FPS)
    
    def cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main() -> None:
    """Main entry point."""
    app = MatrixRainApp()
    
    try:
        if platform.system() == "Emscripten":
            asyncio.ensure_future(app.run())
        else:
            asyncio.run(app.run())
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()