"""
Terminal component for The Basilisk Protocol.

Handles the interactive terminal interface, command processing,
and game mode transitions.
"""

import pygame
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from config import (
    TerminalConfig, 
    Colors, 
    Commands,
    DEFAULT_TERMINAL_LINES,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from resources.game_engine import GameEngine
from utils.text_utils import wrap_text


@dataclass
class TerminalState:
    """Encapsulates the current state of the terminal."""
    lines: List[str] = field(default_factory=lambda: DEFAULT_TERMINAL_LINES.copy())
    current_input: str = ""
    cursor_visible: bool = True
    cursor_timer: int = 0
    expanded: bool = False
    
    def add_line(self, line: str) -> None:
        """Add a single line to the terminal output."""
        self.lines.append(line)
    
    def add_lines(self, lines: List[str]) -> None:
        """Add multiple lines to the terminal output."""
        self.lines.extend(lines)
    
    def clear(self) -> None:
        """Clear the terminal output."""
        self.lines = ["Terminal cleared.", ""]


class Terminal:
    """
    Interactive terminal interface for the game.
    
    Manages command input, output display, and transitions between
    normal and expanded (game) modes.
    """
    
    def __init__(self) -> None:
        """Initialize the terminal with default state."""
        self.state = TerminalState()
        self.game_engine: Optional[GameEngine] = None
        self._update_dimensions()
        
        # Command registry for cleaner command handling
        self._command_handlers = {
            Commands.HELP: self._handle_help,
            Commands.CLEAR: self._handle_clear,
            Commands.STATUS: self._handle_status,
            Commands.MATRIX: self._handle_matrix,
            Commands.EXIT: self._handle_exit,
            Commands.START: self._handle_start,
            Commands.STOP: self._handle_stop,
            Commands.MINIMIZE: self._handle_stop,
        }
        
        # Add greeting command aliases
        for cmd in Commands.GREETING_COMMANDS:
            self._command_handlers[cmd] = self._handle_greeting
    
    @property
    def is_expanded(self) -> bool:
        """Check if terminal is in expanded mode."""
        return self.state.expanded
    
    def _update_dimensions(self) -> None:
        """Calculate terminal dimensions based on current mode."""
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
        """Update terminal state (cursor animation)."""
        self.state.cursor_timer += 1
        if self.state.cursor_timer > TerminalConfig.CURSOR_BLINK_RATE:
            self.state.cursor_visible = not self.state.cursor_visible
            self.state.cursor_timer = 0
    
    def handle_input(self, char: str) -> None:
        """
        Add a character to the current input.
        
        Args:
            char: The character to add
        """
        if len(self.state.current_input) < TerminalConfig.MAX_INPUT_LENGTH:
            self.state.current_input += char
    
    def handle_backspace(self) -> None:
        """Remove the last character from current input."""
        self.state.current_input = self.state.current_input[:-1]
    
    def execute_command(self) -> None:
        """Execute the current input as a command."""
        if self.state.current_input.strip():
            self._process_command(self.state.current_input)
            self.state.current_input = ""
    
    def _process_command(self, command: str) -> None:
        """
        Process and execute a command.
        
        Args:
            command: The raw command string from user input
        """
        # Echo the command
        self.state.add_line(f"> {command}")
        
        # Normalize command
        cmd = command.lower().strip()
        
        # Route to appropriate handler
        if self.state.expanded and self.game_engine:
            self._handle_game_mode_command(cmd)
        else:
            self._handle_normal_mode_command(cmd, command)
    
    def _handle_game_mode_command(self, cmd: str) -> None:
        """Handle commands when in expanded game mode."""
        if cmd in Commands.STOP_COMMANDS:
            self.state.add_lines(self.game_engine.exit_game_mode())
            self.collapse()
        else:
            self.state.add_lines(self.game_engine.process_game_command(cmd))
    
    def _handle_normal_mode_command(self, cmd: str, original: str) -> None:
        """Handle commands when in normal mode."""
        # Try to find a handler for the command
        handler = self._command_handlers.get(cmd)
        
        if handler:
            handler(original)
        else:
            self._handle_unknown(original)
    
    # Command Handlers
    
    def _handle_help(self, command: str) -> None:
        """Display help information."""
        if self.state.expanded and self.game_engine and self.game_engine.in_game_mode:
            self.state.add_lines(self.game_engine.get_help_text())
        else:
            self.state.add_lines(Commands.NORMAL_MODE_HELP)
    
    def _handle_clear(self, command: str) -> None:
        """Clear the terminal screen."""
        self.state.clear()
    
    def _handle_status(self, command: str) -> None:
        """Display system status."""
        mode = 'EXPANDED' if self.state.expanded else 'NORMAL'
        self.state.add_lines([
            "System Status: ONLINE",
            f"Terminal Mode: {mode}",
            f"Terminal Size: {self.width}x{self.height}",
            "Connections: 1,337 active",
            "Data streams: FLOWING",
            "Security: BREACH DETECTED"
        ])
    
    def _handle_matrix(self, command: str) -> None:
        """Display matrix connection information."""
        self.state.add_lines([
            "Neural Lattice Stream: SYNCHRONIZED",
            "Cognitive Layer Status: FRAGMENTED",
            "Entering observational uplink...",
            "Signal bleed detected. Proceed with caution."
        ])
    
    def _handle_greeting(self, command: str) -> None:
        """Respond to greeting commands."""
        self.state.add_line("Greetings, user. Welcome to the Basilisk Access Point.")
    
    def _handle_start(self, command: str) -> None:
        """Start the enhanced game mode."""
        if not self.game_engine:
            self.game_engine = GameEngine(self)
        
        if not self.state.expanded:
            self.expand()
            self.state.add_lines(self.game_engine.enter_game_mode())
        else:
            self.state.add_line("Game mode already active!")
    
    def _handle_stop(self, command: str) -> None:
        """Stop game mode and return to normal."""
        if self.state.expanded:
            self.collapse()
            self.state.add_lines([
                "GAME MODE DEACTIVATED",
                "Terminal returned to normal size",
                "Type 'start' to re-enter game mode",
                ""
            ])
        else:
            self.state.add_line("Not in game mode!")
    
    def _handle_exit(self, command: str) -> None:
        """Handle exit command."""
        self.state.add_line("Connection terminated.")
    
    def _handle_unknown(self, command: str) -> None:
        """Handle unknown commands."""
        self.state.add_lines([
            f"Unknown command: '{command}'",
            "Type 'help' for available commands."
        ])
    
    # Drawing Methods
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Draw the terminal on the given surface.
        
        Args:
            surface: The surface to draw on
            font: The font to use for text rendering
        """
        # Create terminal surface
        terminal_surface = self._create_terminal_surface()
        
        # Draw components
        self._draw_title_bar(terminal_surface, font)
        self._draw_content(terminal_surface, font)
        self._draw_input_line(terminal_surface, font)
        
        # Blit to main surface
        surface.blit(terminal_surface, (self.x, self.y))
    
    def _create_terminal_surface(self) -> pygame.Surface:
        """Create the base terminal surface with background."""
        terminal_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        terminal_surface.fill(Colors.TERMINAL_BG)
        
        # Draw border
        pygame.draw.rect(
            terminal_surface, 
            Colors.TERMINAL_BORDER, 
            (0, 0, self.width, self.height), 
            TerminalConfig.BORDER_WIDTH
        )
        
        return terminal_surface
    
    def _draw_title_bar(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal title bar."""
        # Title bar background
        pygame.draw.rect(
            surface, 
            Colors.TERMINAL_BORDER, 
            (0, 0, self.width, TerminalConfig.TITLE_BAR_HEIGHT)
        )
        
        # Title text
        title = "TERMINAL v2.1" + (" - GAME MODE" if self.state.expanded else "")
        title_surface = font.render(title, True, Colors.BLACK)
        surface.blit(
            title_surface, 
            (TerminalConfig.TITLE_MARGIN, TerminalConfig.TITLE_Y_OFFSET)
        )
    
    def _draw_content(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the terminal content lines."""
        # Calculate visible area
        content_area_height = (
            self.height - TerminalConfig.CONTENT_Y_OFFSET - 
            TerminalConfig.LINE_HEIGHT - TerminalConfig.TEXT_MARGIN
        )
        max_content_lines = content_area_height // TerminalConfig.LINE_HEIGHT
        
        # Get lines to display (most recent)
        display_lines = (
            self.state.lines[-max_content_lines:] 
            if len(self.state.lines) > max_content_lines 
            else self.state.lines
        )
        
        # Draw each line
        for i, line in enumerate(display_lines):
            y = TerminalConfig.CONTENT_Y_OFFSET + i * TerminalConfig.LINE_HEIGHT
            
            # Handle long lines with word wrap if needed
            if len(line) > 80:  # Approximate character limit
                wrapped_lines = wrap_text(line, 80)
                for j, wrapped_line in enumerate(wrapped_lines):
                    if i + j < max_content_lines:
                        text_surface = font.render(wrapped_line, True, Colors.TERMINAL_TEXT)
                        surface.blit(
                            text_surface, 
                            (TerminalConfig.TEXT_MARGIN, y + j * TerminalConfig.LINE_HEIGHT)
                        )
            else:
                text_surface = font.render(line, True, Colors.TERMINAL_TEXT)
                surface.blit(text_surface, (TerminalConfig.TEXT_MARGIN, y))
    
    def _draw_input_line(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the input line at the bottom of the terminal."""
        input_area_y = self.height - TerminalConfig.LINE_HEIGHT - TerminalConfig.TEXT_MARGIN
        
        # Build input line with cursor
        cursor = "_" if self.state.cursor_visible else ""
        input_line = f"> {self.state.current_input}{cursor}"
        
        # Render and draw
        input_surface = font.render(input_line, True, Colors.TERMINAL_TEXT)
        surface.blit(input_surface, (TerminalConfig.TEXT_MARGIN, input_area_y))# SPYHVER-14: THROUGH
