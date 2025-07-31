# # #### Possible changes

# # from enum import Enum
# # from typing import Dict, Tuple

# # class Theme(Enum):
# #     WHITE_BOOT = "white_boot"
# #     MATRIX_BLUE = "matrix_blue"
# #     CYBER_RED = "cyber_red"
# #     GLITCH_MODE = "glitch"
# #     AWAKENING = "awakening"

# # class ThemeColors:
# #     """Color palettes for each theme."""
    
# #     WHITE_BOOT = {
# #         'bg': (245, 245, 245),
# #         'text': (20, 20, 20),
# #         'terminal_bg': (255, 255, 255, 230),
# #         'terminal_border': (180, 180, 180),
# #         'terminal_text': (0, 0, 0),
# #         'stream_primary': (220, 220, 220),
# #         'stream_secondary': (180, 180, 180)
# #     }
    
# #     MATRIX_BLUE = {
# #         'bg': (0, 0, 0),
# #         'text': (100, 200, 255),
# #         'terminal_bg': (10, 15, 25, 180),
# #         'terminal_border': (80, 150, 220),
# #         'terminal_text': (150, 220, 255),
# #         'stream_primary': (100, 200, 255),
# #         'stream_secondary': (50, 120, 180)
# #     }
    
# #     CYBER_RED = {
# #         'bg': (15, 0, 0),
# #         'text': (255, 68, 68),
# #         'terminal_bg': (30, 10, 10, 200),
# #         'terminal_border': (200, 50, 50),
# #         'terminal_text': (255, 100, 100),
# #         'stream_primary': (255, 68, 68),
# #         'stream_secondary': (180, 40, 40)
# #     }
    
# #     @classmethod
# #     def get_palette(cls, theme: Theme) -> Dict[str, Tuple[int, ...]]:
# #         """Get color palette for a specific theme."""
# #         palettes = {
# #             Theme.WHITE_BOOT: cls.WHITE_BOOT,
# #             Theme.MATRIX_BLUE: cls.MATRIX_BLUE,
# #             Theme.CYBER_RED: cls.CYBER_RED,
# #         }
# #         return palettes.get(theme, cls.MATRIX_BLUE)
# # # SPYHVER-25: REALITY

"""
Terminal component for The Basilisk Protocol.

Handles the interactive terminal interface, command processing,
and game mode transitions.
"""

import pygame
import os
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from utils.game_config import (
    TerminalConfig, 
    Colors, 
    Commands,
    DEFAULT_TERMINAL_LINES,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
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
        self.game_engine = None  # Will be initialized when entering game mode
        self.debug_room_to_jump = None  # Store room to jump to in debug mode
        self.debug_mode_active = False  # ADD THIS LINE


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
    
    def add_lines(self, lines: List[str]) -> None:
        """Add multiple lines to the terminal output."""
        self.state.add_lines(lines)
    
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
        
        # Check for debug commands first (simple implementation)
        if command.lower().startswith("boot.debug"):
            self._handle_debug_command(command)
            self.debug_mode_active = False  # Reset flag after first use
            return
        
        if command.lower().startswith("boot.debug"):
            self._handle_debug_command(command)
            return

        # Normalize command
        cmd = command.lower().strip()
        
        # Route to appropriate handler
        if self.state.expanded and self.game_engine:
            self._handle_game_mode_command(cmd)
        else:
            self._handle_normal_mode_command(cmd, command)
    
    def _handle_debug_command(self, command: str) -> None:
        """Handle debug commands directly in terminal."""
        cmd_parts = command.lower().strip().split()
        
        if len(cmd_parts) == 1:
            # Just "boot.debug" - show menu
            self.state.add_lines([
                "=== DEBUG MODE ===",
                "Available debug commands:",
                "",
                "boot.debug list       - List all available rooms",
                "boot.debug jump <room> - Jump directly to a room",
                "",
                "Example: boot.debug jump beacon_1",
                ""
            ])
        elif len(cmd_parts) >= 2:
            action = cmd_parts[1]
            
            if action == "list":
                self._list_available_rooms()
            elif action == "jump" and len(cmd_parts) >= 3:
                room_name = cmd_parts[2]
                self._prepare_debug_jump(room_name)
            else:
                self.state.add_line(f"Unknown debug command: {action}")
    
    def _list_available_rooms(self) -> None:
        """List all rooms in the rooms directory."""
        rooms_dir = "rooms"
        if not os.path.exists(rooms_dir):
            self.state.add_lines(["No rooms directory found!"])
            return
        
        self.state.add_lines([
            "=== AVAILABLE ROOMS ===",
            ""
        ])
        
        # Walk through rooms directory
        room_count = 0
        for root, dirs, files in os.walk(rooms_dir):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('__')]
            
            for filename in files:
                if filename.endswith(".py") and not filename.startswith("__"):
                    room_name = filename[:-3]  # Remove .py
                    if room_name.startswith("rm_"):
                        room_name = room_name[3:]  # Remove rm_ prefix
                    
                    # Show with subdirectory if applicable
                    rel_path = os.path.relpath(root, rooms_dir)
                    if rel_path != ".":
                        self.state.add_line(f"  {rel_path}/{room_name}")
                    else:
                        self.state.add_line(f"  {room_name}")
                    room_count += 1
        
        self.state.add_lines([
            "",
            f"Total rooms: {room_count}",
            "Use 'boot.debug jump <room_name>' to jump to any room."
        ])
    
    def _prepare_debug_jump(self, room_name: str) -> None:
        """Prepare to jump to a room in debug mode."""
        # Check if room file exists (basic check)
        rooms_dir = "rooms"
        room_found = False
        
        # Check main directory and subdirectories
        for root, dirs, files in os.walk(rooms_dir):
            for filename in files:
                if filename.endswith(".py"):
                    check_name = filename[:-3]
                    if check_name.startswith("rm_"):
                        check_name = check_name[3:]
                    
                    if check_name == room_name:
                        room_found = True
                        break
            if room_found:
                break
        
        if not room_found:
            self.state.add_lines([
                f"Room '{room_name}' not found!",
                "Use 'boot.debug list' to see available rooms."
            ])
            return
        
        # Store the room to jump to
        self.debug_room_to_jump = room_name
        
        # Clear terminal for debug jump
        self.state.lines = []  # Clear all lines
        self.state.add_lines([
            f"=== DEBUG JUMP: {room_name.upper()} ===",
            f"Player: [DEBUG]",
            f"Room loaded. Type 'help' for available commands.",
            ""
        ])
        
        # Start game mode with debug flag
        self._handle_start("start")
    
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
        # Lazy import to avoid circular dependency
        from resources.game_engine import GameEngine
        
        if not self.game_engine:
            self.game_engine = GameEngine(self)
        
        if not self.state.expanded:
            self.expand()
            
            # Check if we're doing a debug jump
            if self.debug_room_to_jump:
                # Set debug mode in game state
                self.game_engine.game_state.debug_mode = True
                self.game_engine.game_state.player_name = "[DEBUG]"
                self.game_engine.in_game_mode = True
                
                # Jump to the debug room
                if self.game_engine.game_state.room_exists(self.debug_room_to_jump):
                    self.game_engine.game_state.change_room(self.debug_room_to_jump)
                    # Don't show room entry text - we already showed debug info
                else:
                    self.state.add_line(f"Error: Room '{self.debug_room_to_jump}' not found in game engine!")
                
                # Clear the debug jump flag
                self.debug_room_to_jump = None
            else:
                # Normal game start
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
        surface.blit(input_surface, (TerminalConfig.TEXT_MARGIN, input_area_y))

# SPYHVER-14: ACROSS