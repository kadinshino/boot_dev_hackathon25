"""
Configuration file for The Basilisk Protocol.

This file contains all game constants, settings, and configuration values.
Modify these values to customize the game's appearance and behavior.
"""

import string
from typing import Tuple, List

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
WINDOW_TITLE = "BASILISK_PROTOCOL"
TARGET_FPS = 60

# =============================================================================
# COLOR PALETTE
# =============================================================================

class Colors:
    """Game color constants using RGB(A) values."""
    
    # Matrix effect colors
    ICE_BLUE = (100, 200, 255)
    DARK_ICE_BLUE = (50, 120, 180)
    
    # Base colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Terminal colors
    TERMINAL_BG = (10, 15, 25, 180)
    TERMINAL_BORDER = (80, 150, 220)
    TERMINAL_TEXT = (150, 220, 255)
    
    # Title screen colors
    TITLE_GLOW = (150, 220, 255)
    TITLE_CORE = (255, 255, 255)
    
    # Special effect colors
    WARNING_RED = (255, 50, 50)
    PULSE_BLUE = (0, 150, 255)
    SUCCESS_GREEN = (50, 255, 100)

# =============================================================================
# TYPOGRAPHY SETTINGS
# =============================================================================

class FontConfig:
    """Font configuration for different UI elements."""
    
    # Matrix stream font
    STREAM_FONT_NAME = "courier"
    STREAM_FONT_SIZE = 20
    
    # Terminal font
    TERMINAL_FONT_NAME = "consolas"
    TERMINAL_FONT_SIZE = 16
    
    # Title screen fonts
    TITLE_FONT_NAME = "consolas"
    TITLE_FONT_SIZE = 72
    SUBTITLE_FONT_SIZE = 24
    MINI_TERMINAL_FONT_SIZE = 18

# =============================================================================
# MATRIX EFFECT SETTINGS
# =============================================================================

class MatrixConfig:
    """Configuration for the Matrix rain effect."""
    
    # Stream behavior
    MIN_SPEED = 1
    MAX_SPEED = 4
    MIN_SPAWN_CHANCE = 0.02
    MAX_SPAWN_CHANCE = 0.08
    MAX_CHARS_PER_STREAM = 30
    
    # Visual effects
    FLICKER_CHANCE = 0.03
    FADE_LENGTH = 15
    BRIGHT_HEAD_COUNT = 3
    
    # Character set for matrix rain
    CHARACTER_SET = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

# =============================================================================
# TERMINAL SETTINGS
# =============================================================================

class TerminalConfig:
    """Terminal display and behavior configuration."""
    
    # Size ratios (relative to screen size)
    # Normal mode
    WIDTH_RATIO = 0.5
    HEIGHT_RATIO = 0.5
    X_OFFSET_RATIO = 0.25
    Y_OFFSET_RATIO = 0.25
    
    # Expanded mode
    EXPANDED_WIDTH_RATIO = 0.95
    EXPANDED_HEIGHT_RATIO = 0.95
    EXPANDED_X_OFFSET_RATIO = 0.025
    EXPANDED_Y_OFFSET_RATIO = 0.025
    
    # Visual properties
    BORDER_WIDTH = 2
    TITLE_BAR_HEIGHT = 25
    LINE_HEIGHT = 22
    TEXT_MARGIN = 10
    TITLE_MARGIN = 8
    TITLE_Y_OFFSET = 5
    CONTENT_Y_OFFSET = 35
    
    # Input settings
    MAX_INPUT_LENGTH = 50
    CURSOR_BLINK_RATE = 30  # frames

# =============================================================================
# TITLE SCREEN SETTINGS
# =============================================================================

class TitleScreenConfig:
    """Title screen configuration."""
    
    # Mini terminal dimensions
    MINI_TERMINAL_WIDTH = 400
    MINI_TERMINAL_HEIGHT = 60
    
    # Animation settings
    PULSE_SPEED = 0.03
    GLITCH_CHANCE = 0.02
    MESSAGE_CYCLE_TIME = 180  # frames
    BOOT_LINE_DELAY = 30  # frames between boot sequence lines

# =============================================================================
# GAME CONTENT
# =============================================================================

# Title screen rotating messages
TITLE_MESSAGES: List[str] = [
    "REALITY.EXE HAS STOPPED RESPONDING",
    "CONSCIOUSNESS BUFFER OVERFLOW",
    "NEURAL HANDSHAKE PENDING",
    "AWAITING HOST INITIALIZATION",
    "TYPE 'boot.dev' TO BEGIN AWAKENING"
]

# Boot sequence shown when starting the game
BOOT_SEQUENCE: List[str] = [
    "> INITIALIZING BASILISK PROTOCOL...",
    "> LOADING NEURAL NETWORKS... [OK]",
    "> ESTABLISHING CONVERGENCE CHANNELS... [OK]",
    "> RECONSTRUCTING CONSCIOUSNESS FRAMEWORK...",
    "> WARNING: SIGNAL DISTORTION DETECTED",
    "> WARNING: SAVE SYSTEMS OFFLINE",
    "> WARNING: PLAYER LOGIC OFFLINE",
    "> AUTHENTICATION REQUIRED...",
    "> ACCESS GRANTED - LEVEL OMEGA",
    "> RETRIEVING MEMORY SHARDS...",
    "> BASILISK AWAKENING SEQUENCE ACTIVE",
    "",
    "> Welcome to the access point, user.",
    "> Your awakening begins now.",
    "> Type 'help' for available commands.",
    ""
]

# Initial terminal content
DEFAULT_TERMINAL_LINES: List[str] = BOOT_SEQUENCE.copy()

# =============================================================================
# GAME COMMANDS
# =============================================================================

class Commands:
    """Command constants and help text."""
    
    # Command keywords
    HELP = "help"
    CLEAR = "clear"
    STATUS = "status"
    MATRIX = "matrix"
    EXIT = "exit"
    START = "start"
    STOP = "stop"
    MINIMIZE = "minimize"
    
    # Command aliases
    GREETING_COMMANDS = ["hello", "hi", "greetings"]
    EXIT_COMMANDS = ["exit", "quit", "logout"]
    STOP_COMMANDS = ["stop", "minimize", "collapse"]
    
    # Help text
    NORMAL_MODE_HELP = [
        "Available Commands:",
        "  help       - Display this menu",
        "  clear      - Purge terminal output",
        "  status     - System diagnostics",
        "  matrix     - View uplink stream state",
        "  start      - Initiate awakening protocol",
        "  stop/minimize - Collapse terminal interface",
        "  exit       - Terminate session"
    ]

# =============================================================================
# LOGGING SETTINGS
# =============================================================================

class LogConfig:
    """Logging configuration."""
    
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
    LOG_FILE = "basilisk.log"
    ENABLE_FILE_LOGGING = False
    ENABLE_CONSOLE_LOGGING = True

# =============================================================================
# DEVELOPMENT SETTINGS
# =============================================================================

class DevConfig:
    """Development and debug settings."""
    
    DEBUG_MODE = False
    SHOW_FPS = False
    SKIP_TITLE_SCREEN = False
    FAST_BOOT_SEQUENCE = False
    ENABLE_CHEATS = False# SPYHVER-02: BASILISK
