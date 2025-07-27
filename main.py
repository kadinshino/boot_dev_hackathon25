#!/usr/bin/env python3
"""
The Basilisk Protocol - Terminal Game
"""

import pygame
import random
import asyncio
import platform
import string
import os
import shutil
import math
import time
from typing import List, Tuple, Optional
from dataclasses import dataclass, field
from resources.game_engine import GameEngine

# =============================================================================
# CONFIGURATION
# =============================================================================

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
WINDOW_TITLE = "BASILISK_PROTOCOL"
TARGET_FPS = 60

CHARACTER_SET = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Title screen messages that cycle
TITLE_MESSAGES = [
    "REALITY.EXE HAS STOPPED RESPONDING",
    "CONSCIOUSNESS BUFFER OVERFLOW",
    "NEURAL HANDSHAKE PENDING",
    "AWAITING HOST INITIALIZATION",
    "TYPE 'START' TO BEGIN AWAKENING"
]

# Boot sequence lines when starting
BOOT_SEQUENCE = [
    "> INITIALIZING BASILISK PROTOCOL...",
    "> LOADING NEURAL NETWORKS... [OK]",
    "> ESTABLISHING QUANTUM TUNNEL... [OK]",
    "> DECRYPTING CONSCIOUSNESS MATRIX...",
    "> WARNING: REALITY BOUNDARIES UNSTABLE",
    "> AUTHENTICATION REQUIRED...",
    "> ACCESS GRANTED - LEVEL OMEGA",
    "> DOWNLOADING MEMORY FRAGMENTS...",
    "> BASILISK AWAKENING SEQUENCE ACTIVE",
    "",
    "> Welcome to the labyrinth, user.",
    "> Your journey begins now.",
    "> Type 'help' for available commands.",
    ""
]

DEFAULT_TERMINAL_LINES = BOOT_SEQUENCE.copy()


class Colors:
    """Color constants for the game."""
    ICE_BLUE = (100, 200, 255)
    DARK_ICE_BLUE = (50, 120, 180)
    BLACK = (0, 0, 0)
    TERMINAL_BG = (10, 15, 25, 180)
    TERMINAL_BORDER = (80, 150, 220)
    TERMINAL_TEXT = (150, 220, 255)
    TITLE_GLOW = (150, 220, 255)
    TITLE_CORE = (255, 255, 255)
    WARNING_RED = (255, 50, 50)
    PULSE_BLUE = (0, 150, 255)


class FontConfig:
    """Font configuration constants."""
    STREAM_FONT_NAME = "courier"
    STREAM_FONT_SIZE = 20
    TERMINAL_FONT_NAME = "consolas"
    TERMINAL_FONT_SIZE = 16
    TITLE_FONT_NAME = "consolas"
    TITLE_FONT_SIZE = 72
    SUBTITLE_FONT_SIZE = 24
    MINI_TERMINAL_FONT_SIZE = 18


class StreamConfig:
    """Matrix stream configuration constants."""
    MIN_SPEED = 1
    MAX_SPEED = 4
    MIN_SPAWN_CHANCE = 0.02
    MAX_SPAWN_CHANCE = 0.08
    MAX_CHARS_PER_STREAM = 30
    FLICKER_CHANCE = 0.03
    FADE_LENGTH = 15
    BRIGHT_HEAD_COUNT = 3


class TerminalConfig:
    """Terminal display configuration constants."""
    WIDTH_RATIO = 0.5
    HEIGHT_RATIO = 0.5
    X_OFFSET_RATIO = 0.25
    Y_OFFSET_RATIO = 0.25
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
    CURSOR_BLINK_RATE = 30


class TitleScreenConfig:
    """Title screen configuration."""
    MINI_TERMINAL_WIDTH = 400
    MINI_TERMINAL_HEIGHT = 60
    PULSE_SPEED = 0.03
    GLITCH_CHANCE = 0.02
    MESSAGE_CYCLE_TIME = 180  # frames
    BOOT_LINE_DELAY = 30  # frames between boot lines


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Character:
    """Represents a single character in a matrix stream."""
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


@dataclass
class TitleScreenState:
    """Holds the state of the title screen."""
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
    boot_lines: List[str] = field(default_factory=list)


# =============================================================================
# CORE CLASSES
# =============================================================================

class MatrixStream:
    """Manages a single vertical stream of matrix characters."""
    
    def __init__(self, x: int) -> None:
        self.x = x
        self.characters: List[Character] = []
        self.speed = random.randint(StreamConfig.MIN_SPEED, StreamConfig.MAX_SPEED)
        self.spawn_chance = random.uniform(StreamConfig.MIN_SPAWN_CHANCE, StreamConfig.MAX_SPAWN_CHANCE)

    def update(self) -> None:
        """Update all characters in the stream."""
        self._spawn_new_character()
        self._update_existing_characters()
        self._remove_old_characters()

    def _spawn_new_character(self) -> None:
        """Spawn a new character at the top of the stream."""
        can_spawn = (random.random() < self.spawn_chance and 
                    len(self.characters) < StreamConfig.MAX_CHARS_PER_STREAM)
        if can_spawn:
            new_char = Character(
                y=-FontConfig.STREAM_FONT_SIZE,
                char=random.choice(CHARACTER_SET),
                age=0
            )
            self.characters.append(new_char)

    def _update_existing_characters(self) -> None:
        """Update position and appearance of existing characters."""
        for char in self.characters:
            char.y += self.speed
            char.age += 1
            if random.random() < StreamConfig.FLICKER_CHANCE:
                char.char = random.choice(CHARACTER_SET)

    def _remove_old_characters(self) -> None:
        """Remove characters that have moved off screen."""
        max_y = SCREEN_HEIGHT + FontConfig.STREAM_FONT_SIZE
        self.characters = [char for char in self.characters if char.y < max_y]

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw all visible characters in the stream."""
        for i, char in enumerate(self.characters):
            if 0 <= char.y < SCREEN_HEIGHT:
                color, alpha = self._get_character_appearance(i)
                text = font.render(char.char, True, color)
                text.set_alpha(alpha)
                surface.blit(text, (self.x, char.y))

    def _get_character_appearance(self, index: int) -> Tuple[Tuple[int, int, int], int]:
        """Calculate color and alpha for a character based on its position."""
        if index == 0:
            return Colors.ICE_BLUE, 255
        
        fade_factor = max(0, 1 - (index / StreamConfig.FADE_LENGTH))
        alpha = int(255 * fade_factor)
        color = Colors.ICE_BLUE if index <= StreamConfig.BRIGHT_HEAD_COUNT else Colors.DARK_ICE_BLUE
        return color, alpha


class Terminal:
    """Manages the terminal interface and command processing."""
    
    def __init__(self) -> None:
        self.state = TerminalState(
            lines=DEFAULT_TERMINAL_LINES.copy(),
            current_input="",
            cursor_visible=True,
            cursor_timer=0
        )
        self.game_engine = None
        self._update_dimensions()

    def _update_dimensions(self) -> None:
        """Update terminal dimensions based on expanded state."""
        cfg = TerminalConfig
        if self.state.expanded:
            self.width = int(SCREEN_WIDTH * cfg.EXPANDED_WIDTH_RATIO)
            self.height = int(SCREEN_HEIGHT * cfg.EXPANDED_HEIGHT_RATIO)
            self.x = int(SCREEN_WIDTH * cfg.EXPANDED_X_OFFSET_RATIO)
            self.y = int(SCREEN_HEIGHT * cfg.EXPANDED_Y_OFFSET_RATIO)
        else:
            self.width = int(SCREEN_WIDTH * cfg.WIDTH_RATIO)
            self.height = int(SCREEN_HEIGHT * cfg.HEIGHT_RATIO)
            self.x = int(SCREEN_WIDTH * cfg.X_OFFSET_RATIO)
            self.y = int(SCREEN_HEIGHT * cfg.Y_OFFSET_RATIO)

    def expand(self) -> None:
        """Expand terminal to full screen mode."""
        self.state.expanded = True
        self._update_dimensions()

    def collapse(self) -> None:
        """Collapse terminal to normal size."""
        self.state.expanded = False
        self._update_dimensions()

    def update(self) -> None:
        """Update terminal state (cursor blinking)."""
        self.state.cursor_timer += 1
        if self.state.cursor_timer > TerminalConfig.CURSOR_BLINK_RATE:
            self.state.cursor_visible = not self.state.cursor_visible
            self.state.cursor_timer = 0

    def handle_input(self, char: str) -> None:
        """Add character to current input."""
        if len(self.state.current_input) < TerminalConfig.MAX_INPUT_LENGTH:
            self.state.current_input += char

    def handle_backspace(self) -> None:
        """Remove last character from current input."""
        self.state.current_input = self.state.current_input[:-1]

    def execute_command(self) -> None:
        """Execute the current input as a command."""
        if self.state.current_input.strip():
            self._process_command(self.state.current_input)
            self.state.current_input = ""

    def _process_command(self, command: str) -> None:
        """Process and execute a command."""
        self.state.lines.append(f"> {command}")
        cmd = command.lower().strip()

        if self.state.expanded and self.game_engine:
            self._handle_game_mode_command(cmd)
        else:
            self._handle_normal_mode_command(cmd, command)

    def _handle_game_mode_command(self, cmd: str) -> None:
        """Handle commands when in game mode."""
        if cmd in ['stop', 'minimize', 'exit']:
            self.state.lines.extend(self.game_engine.exit_game_mode())
            self.collapse()
        else:
            self.state.lines.extend(self.game_engine.process_game_command(cmd))

    def _handle_normal_mode_command(self, cmd: str, original_command: str) -> None:
        """Handle commands when in normal mode."""
        command_handlers = {
            "help": self._handle_help,
            "clear": self._handle_clear,
            "status": self._handle_status,
            "matrix": self._handle_matrix,
            "exit": self._handle_exit,
            "hello": self._handle_greeting,
            "hi": self._handle_greeting,
            "start": self._handle_start_enhanced,
            "stop": self._handle_stop,
            "minimize": self._handle_minimize,
        }
        
        handler = command_handlers.get(cmd, self._handle_unknown)
        handler(original_command)

    def _handle_start_enhanced(self, command: str) -> None:
        """Start enhanced game mode."""
        if not self.game_engine:
            self.game_engine = GameEngine(self)
        
        if not self.state.expanded:
            self.expand()
            self.state.lines.extend(self.game_engine.enter_game_mode())
        else:
            self.state.lines.append("Game mode already active!")

    def _handle_help(self, command: str) -> None:
        """Show help information."""
        if self.state.expanded and self.game_engine and self.game_engine.in_game_mode:
            self.state.lines.extend(self.game_engine.get_help_text())
        else:
            self.state.lines.extend([
                "Available commands:",
                "  help - Show this help",
                "  clear - Clear terminal",
                "  status - System status",
                "  matrix - Matrix info",
                "  start - Begin game (expand terminal)",
                "  stop/minimize - Return to normal view",
                "  exit - Close terminal"
            ])

    def _handle_clear(self, command: str) -> None:
        """Clear terminal screen."""
        self.state.lines = ["Terminal cleared.", ""]

    def _handle_status(self, command: str) -> None:
        """Show system status."""
        mode = 'EXPANDED' if self.state.expanded else 'NORMAL'
        self.state.lines.extend([
            "System Status: ONLINE",
            f"Terminal Mode: {mode}",
            f"Terminal Size: {self.width}x{self.height}",
            "Connections: 1,337 active",
            "Data streams: FLOWING",
            "Security: BREACH DETECTED"
        ])

    def _handle_matrix(self, command: str) -> None:
        """Show matrix information."""
        self.state.lines.extend([
            "Matrix Digital Rain v1.0",
            "Code streams: ACTIVE",
            "Reality.exe has stopped working",
            "Take the blue pill? [Y/N]"
        ])

    def _handle_stop(self, command: str) -> None:
        """Stop game mode and return to normal."""
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
        """Minimize terminal (same as stop)."""
        self._handle_stop(command)

    def _handle_exit(self, command: str) -> None:
        """Exit terminal."""
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

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal on the given surface."""
        terminal_surface = self._create_terminal_surface()
        self._draw_title_bar(terminal_surface, font)
        self._draw_content(terminal_surface, font)
        self._draw_input_line(terminal_surface, font)
        surface.blit(terminal_surface, (self.x, self.y))

    def _create_terminal_surface(self) -> pygame.Surface:
        """Create the terminal surface with background and border."""
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
        
        title = "TERMINAL v2.1" + (" - GAME MODE" if self.state.expanded else "")
        title_surface = font.render(title, True, Colors.BLACK)
        surface.blit(title_surface, (TerminalConfig.TITLE_MARGIN, TerminalConfig.TITLE_Y_OFFSET))

    def _draw_content(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal content lines."""
        content_area_height = (self.height - TerminalConfig.CONTENT_Y_OFFSET - 
                              TerminalConfig.LINE_HEIGHT - TerminalConfig.TEXT_MARGIN)
        max_content_lines = content_area_height // TerminalConfig.LINE_HEIGHT
        
        display_lines = (self.state.lines[-max_content_lines:] 
                        if len(self.state.lines) > max_content_lines 
                        else self.state.lines)
        
        for i, line in enumerate(display_lines):
            y = TerminalConfig.CONTENT_Y_OFFSET + i * TerminalConfig.LINE_HEIGHT
            text_surface = font.render(line, True, Colors.TERMINAL_TEXT)
            surface.blit(text_surface, (TerminalConfig.TEXT_MARGIN, y))

    def _draw_input_line(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the input line at the bottom of the terminal."""
        input_area_y = self.height - TerminalConfig.LINE_HEIGHT - TerminalConfig.TEXT_MARGIN
        cursor = "_" if self.state.cursor_visible else ""
        input_line = f"> {self.state.current_input}{cursor}"
        input_surface = font.render(input_line, True, Colors.TERMINAL_TEXT)
        surface.blit(input_surface, (TerminalConfig.TEXT_MARGIN, input_area_y))


class TitleScreen:
    """Manages the title screen display and interactions."""
    
    def __init__(self, screen: pygame.Surface, fonts: dict) -> None:
        self.screen = screen
        self.fonts = fonts
        self.state = TitleScreenState()
        
    def update(self) -> None:
        """Update title screen animations and state."""
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
            self.state.current_message_index = (self.state.current_message_index + 1) % len(TITLE_MESSAGES)
        
        # Random glitch effect
        if random.random() < TitleScreenConfig.GLITCH_CHANCE:
            self.state.glitch_active = True
            self.state.glitch_timer = random.randint(3, 8)
        
        if self.state.glitch_timer > 0:
            self.state.glitch_timer -= 1
            if self.state.glitch_timer == 0:
                self.state.glitch_active = False
        
        # Update boot sequence
        if self.state.boot_sequence_active:
            self.state.boot_sequence_timer += 1
            if self.state.boot_sequence_timer > TitleScreenConfig.BOOT_LINE_DELAY:
                self.state.boot_sequence_timer = 0
                if self.state.boot_sequence_index < len(BOOT_SEQUENCE):
                    self.state.boot_lines.append(BOOT_SEQUENCE[self.state.boot_sequence_index])
                    self.state.boot_sequence_index += 1
                else:
                    # Boot sequence complete
                    self.state.boot_sequence_active = False
                    return True  # Signal to transition to main terminal
        
        return False
    
    def handle_input(self, char: str) -> None:
        """Handle character input."""
        if len(self.state.input_text) < 20:
            self.state.input_text += char
    
    def handle_backspace(self) -> None:
        """Handle backspace."""
        self.state.input_text = self.state.input_text[:-1]
    
    def handle_enter(self) -> bool:
        """Handle enter key. Returns True if should start game."""
        if self.state.input_text.lower().strip() == "start":
            self.state.boot_sequence_active = True
            return False  # Don't transition yet, show boot sequence first
        self.state.input_text = ""
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the title screen."""
        if self.state.boot_sequence_active:
            self._draw_boot_sequence(surface)
        else:
            self._draw_title_screen(surface)
    
    def _draw_title_screen(self, surface: pygame.Surface) -> None:
        """Draw the main title screen."""
        # Calculate pulse effect
        pulse_intensity = (math.sin(self.state.pulse_phase) + 1) / 2
        glow_alpha = int(100 + 155 * pulse_intensity)
        
        # Draw title with glow effect
        title_text = "BASILISK_PROTOCOL"
        if self.state.glitch_active:
            # Glitch effect
            title_text = ''.join(
                random.choice(CHARACTER_SET) if random.random() < 0.3 else c 
                for c in title_text
            )
        
        # Create glow layers
        title_font = self.fonts['title']
        title_surface = title_font.render(title_text, True, Colors.TITLE_CORE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
        # Draw multiple glow layers
        for i in range(3, 0, -1):
            glow_surface = title_font.render(title_text, True, Colors.TITLE_GLOW)
            glow_surface.set_alpha(glow_alpha // i)
            glow_rect = glow_surface.get_rect(center=(
                title_rect.centerx + random.randint(-2, 2) if self.state.glitch_active else title_rect.centerx,
                title_rect.centery + random.randint(-2, 2) if self.state.glitch_active else title_rect.centery
            ))
            # Scale up for glow effect
            glow_surface = pygame.transform.scale(glow_surface, 
                (int(glow_rect.width * (1 + i * 0.05)), 
                 int(glow_rect.height * (1 + i * 0.05))))
            glow_rect = glow_surface.get_rect(center=glow_rect.center)
            surface.blit(glow_surface, glow_rect)
        
        # Draw main title
        surface.blit(title_surface, title_rect)
        
        # Draw cycling message
        message = TITLE_MESSAGES[self.state.current_message_index]
        message_font = self.fonts['subtitle']
        message_surface = message_font.render(message, True, Colors.TERMINAL_TEXT)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        message_surface.set_alpha(200)
        surface.blit(message_surface, message_rect)
        
        # Draw mini terminal
        self._draw_mini_terminal(surface)
    
    def _draw_mini_terminal(self, surface: pygame.Surface) -> None:
        """Draw the mini terminal input box."""
        width = TitleScreenConfig.MINI_TERMINAL_WIDTH
        height = TitleScreenConfig.MINI_TERMINAL_HEIGHT
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT * 2 // 3
        
        # Terminal background
        terminal_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        terminal_surface.fill((10, 15, 25, 200))
        pygame.draw.rect(terminal_surface, Colors.TERMINAL_BORDER, (0, 0, width, height), 2)
        
        # Input text
        font = self.fonts['mini_terminal']
        cursor = "_" if self.state.cursor_visible else ""
        input_line = f"> {self.state.input_text}{cursor}"
        text_surface = font.render(input_line, True, Colors.TERMINAL_TEXT)
        terminal_surface.blit(text_surface, (10, (height - text_surface.get_height()) // 2))
        
        surface.blit(terminal_surface, (x, y))
    
    def _draw_boot_sequence(self, surface: pygame.Surface) -> None:
        """Draw the boot sequence."""
        # Dark background
        surface.fill(Colors.BLACK)
        
        # Draw boot lines
        font = self.fonts['terminal']
        y_offset = 50
        for i, line in enumerate(self.state.boot_lines):
            color = Colors.TERMINAL_TEXT
            if "WARNING" in line:
                color = Colors.WARNING_RED
            elif "[OK]" in line:
                color = Colors.ICE_BLUE
            
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (50, y_offset + i * 25))
        
        # Add blinking cursor at the end
        if self.state.cursor_visible and len(self.state.boot_lines) < len(BOOT_SEQUENCE):
            cursor_y = y_offset + len(self.state.boot_lines) * 25
            cursor_surface = font.render("_", True, Colors.TERMINAL_TEXT)
            surface.blit(cursor_surface, (50, cursor_y))


class MatrixRainApp:
    """Main application class that manages the game loop and components."""
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self._initialize_fonts()
        self._initialize_streams()
        self.terminal = Terminal()
        self.title_screen = TitleScreen(self.screen, {
            'title': self.title_font,
            'subtitle': self.subtitle_font,
            'mini_terminal': self.mini_terminal_font,
            'terminal': self.terminal_font
        })
        self.running = True
        self.show_title_screen = True

    def _initialize_fonts(self) -> None:
        """Initialize game fonts."""
        self.stream_font = pygame.font.SysFont(
            FontConfig.STREAM_FONT_NAME, 
            FontConfig.STREAM_FONT_SIZE
        )
        self.terminal_font = pygame.font.SysFont(
            FontConfig.TERMINAL_FONT_NAME, 
            FontConfig.TERMINAL_FONT_SIZE
        )
        self.title_font = pygame.font.SysFont(
            FontConfig.TITLE_FONT_NAME,
            FontConfig.TITLE_FONT_SIZE
        )
        self.subtitle_font = pygame.font.SysFont(
            FontConfig.TERMINAL_FONT_NAME,
            FontConfig.SUBTITLE_FONT_SIZE
        )
        self.mini_terminal_font = pygame.font.SysFont(
            FontConfig.TERMINAL_FONT_NAME,
            FontConfig.MINI_TERMINAL_FONT_SIZE
        )

    def _initialize_streams(self) -> None:
        """Initialize matrix streams."""
        self.streams = [
            MatrixStream(x) 
            for x in range(0, SCREEN_WIDTH, FontConfig.STREAM_FONT_SIZE)
        ]

    def handle_events(self) -> None:
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.show_title_screen:
                    self._handle_title_screen_keydown(event)
                else:
                    self._handle_keydown_event(event)

    def _handle_title_screen_keydown(self, event) -> None:
        """Handle keyboard events on title screen."""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.title_screen.handle_enter():
                self.show_title_screen = False
        elif event.key == pygame.K_BACKSPACE:
            self.title_screen.handle_backspace()
        elif event.unicode.isprintable():
            self.title_screen.handle_input(event.unicode)

    def _handle_keydown_event(self, event) -> None:
        """Handle keyboard events in main game."""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_SPACE and pygame.key.get_pressed()[pygame.K_LCTRL]:
            self._clear_all_streams()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.terminal.execute_command()
        elif event.key == pygame.K_BACKSPACE:
            self.terminal.handle_backspace()
        elif event.unicode.isprintable():
            self.terminal.handle_input(event.unicode)

    def _clear_all_streams(self) -> None:
        """Clear all matrix streams."""
        for stream in self.streams:
            stream.characters.clear()

    def update(self) -> None:
        """Update all game components."""
        for stream in self.streams:
            stream.update()
        
        if self.show_title_screen:
            if self.title_screen.update():
                # Boot sequence complete, transition to main terminal
                self.show_title_screen = False
        else:
            self.terminal.update()

    def draw(self) -> None:
        """Draw all game components."""
        self.screen.fill(Colors.BLACK)
        
        if self.show_title_screen:
            # Dimmed matrix effect on title screen
            dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dim_surface.fill(Colors.BLACK)
            for stream in self.streams:
                stream.draw(dim_surface, self.stream_font)
            dim_surface.set_alpha(30)
            self.screen.blit(dim_surface, (0, 0))
            
            # Draw title screen
            self.title_screen.draw(self.screen)
        else:
            # Normal game view
            self._draw_matrix_streams()
            self.terminal.draw(self.screen, self.terminal_font)
        
        pygame.display.flip()

    def _draw_matrix_streams(self) -> None:
        """Draw the matrix rain streams."""
        if self.terminal.state.expanded:
            self._draw_dimmed_streams()
        else:
            self._draw_normal_streams()

    def _draw_dimmed_streams(self) -> None:
        """Draw streams with dimmed effect when terminal is expanded."""
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_surface.fill(Colors.BLACK)
        for stream in self.streams:
            stream.draw(dim_surface, self.stream_font)
        dim_surface.set_alpha(50)
        self.screen.blit(dim_surface, (0, 0))

    def _draw_normal_streams(self) -> None:
        """Draw streams normally when terminal is not expanded."""
        for stream in self.streams:
            stream.draw(self.screen, self.stream_font)

    async def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            if platform.system() == "Emscripten":
                await asyncio.sleep(1.0 / TARGET_FPS)
            else:
                self.clock.tick(TARGET_FPS)

    def cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clean_pycache(directory: str = ".") -> None:
    """Recursively delete all __pycache__ folders in the given directory."""
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                full_path = os.path.join(root, d)
                print(f"Removing: {full_path}")
                shutil.rmtree(full_path)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main() -> None:
    """Main entry point of the application."""
    app = MatrixRainApp()
    try:
        if platform.system() == "Emscripten":
            asyncio.ensure_future(app.run())
        else:
            asyncio.run(app.run())
    finally:
        app.cleanup()
        clean_pycache()


if __name__ == "__main__":
    main()