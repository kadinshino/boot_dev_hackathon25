

# utils/text_utils.py
"""
Text processing utilities for The Basilisk Protocol.

Provides functions for text wrapping, truncation, and sanitization.
"""

from typing import List, Optional
import re
import unicodedata


def wrap_text(text: str, max_width: int, preserve_words: bool = True) -> List[str]:
    """
    Wrap text to fit within a maximum width.
    
    Args:
        text: The text to wrap
        max_width: Maximum characters per line
        preserve_words: If True, avoid breaking words
        
    Returns:
        List of wrapped lines
    """
    if not text:
        return []
    
    # Handle newlines in input
    paragraphs = text.split('\n')
    all_lines = []
    
    for paragraph in paragraphs:
        if not paragraph:
            all_lines.append('')
            continue
            
        if preserve_words:
            words = paragraph.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word)
                
                # If adding this word would exceed the limit
                if current_length + word_length + len(current_line) > max_width:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = word_length
                    else:
                        # Word is too long, force break it
                        while len(word) > max_width:
                            lines.append(word[:max_width])
                            word = word[max_width:]
                        if word:
                            current_line = [word]
                            current_length = len(word)
                else:
                    current_line.append(word)
                    current_length += word_length
            
            # Add remaining words
            if current_line:
                lines.append(' '.join(current_line))
            
            all_lines.extend(lines)
        else:
            # Simple character wrapping
            while paragraph:
                all_lines.append(paragraph[:max_width])
                paragraph = paragraph[max_width:]
    
    return all_lines


def truncate_text(
    text: str, 
    max_length: int, 
    suffix: str = "...",
    preserve_words: bool = True
) -> str:
    """
    Truncate text to a maximum length with suffix.
    
    Args:
        text: The text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncating
        preserve_words: If True, truncate at word boundary
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= len(suffix):
        return suffix[:max_length]
    
    truncate_at = max_length - len(suffix)
    
    if preserve_words:
        # Find the last space before truncate_at
        space_index = text.rfind(' ', 0, truncate_at)
        if space_index > 0:
            truncate_at = space_index
    
    return text[:truncate_at].rstrip() + suffix


def sanitize_input(text: str, max_length: int = 100) -> str:
    """
    Sanitize user input by removing dangerous characters.
    
    Args:
        text: Raw user input
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove control characters and normalize unicode
    text = unicodedata.normalize('NFKC', text)
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Remove multiple spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    return sanitized.strip()


def highlight_text(text: str, highlight: str, marker: str = '*') -> str:
    """
    Highlight occurrences of a substring in text.
    
    Args:
        text: The text to search in
        highlight: The substring to highlight
        marker: Character to use for highlighting
        
    Returns:
        Text with highlighted substrings
    """
    if not highlight or not text:
        return text
    
    # Case-insensitive highlighting
    pattern = re.compile(re.escape(highlight), re.IGNORECASE)
    return pattern.sub(f"{marker}\\g<0>{marker}", text)


def remove_ansi_codes(text: str) -> str:
    """
    Remove ANSI escape codes from text.
    
    Args:
        text: Text potentially containing ANSI codes
        
    Returns:
        Clean text without ANSI codes
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
