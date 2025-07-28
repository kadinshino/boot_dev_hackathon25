

# utils/logging.py
"""
Logging utilities for The Basilisk Protocol.

Provides configured logging for debugging and development.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import from config - this assumes config.py exists
try:
    from config import LogConfig
except ImportError:
    # Fallback configuration if config.py isn't available
    class LogConfig:
        LOG_LEVEL = "INFO"
        LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
        LOG_FILE = "basilisk.log"
        ENABLE_FILE_LOGGING = False
        ENABLE_CONSOLE_LOGGING = True


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds color to console output.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to the level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        # Format the message
        result = super().format(record)
        
        # Reset levelname for other handlers
        record.levelname = levelname
        
        return result


def setup_logging(
    name: str = 'basilisk',
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up the logging configuration.
    
    Args:
        name: Logger name
        log_level: Override log level from config
        log_file: Override log file from config
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Use provided level or fall back to config
    level = log_level or LogConfig.LOG_LEVEL
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with color
    if LogConfig.ENABLE_CONSOLE_LOGGING:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            ColoredFormatter(LogConfig.LOG_FORMAT)
        )
        logger.addHandler(console_handler)
    
    # File handler
    if LogConfig.ENABLE_FILE_LOGGING:
        file_path = log_file or LogConfig.LOG_FILE
        
        # Create log directory if needed
        log_dir = Path(file_path).parent
        if log_dir.name:
            log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(
            logging.Formatter(LogConfig.LOG_FORMAT)
        )
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logging()


# Convenience functions
def log_debug(message: str, *args, **kwargs):
    """Log a debug message."""
    logger.debug(message, *args, **kwargs)


def log_info(message: str, *args, **kwargs):
    """Log an info message."""
    logger.info(message, *args, **kwargs)


def log_warning(message: str, *args, **kwargs):
    """Log a warning message."""
    logger.warning(message, *args, **kwargs)


def log_error(message: str, *args, **kwargs):
    """Log an error message."""
    logger.error(message, *args, **kwargs)


def log_critical(message: str, *args, **kwargs):
    """Log a critical message."""
    logger.critical(message, *args, **kwargs)
# SPYHVER-49: TO
