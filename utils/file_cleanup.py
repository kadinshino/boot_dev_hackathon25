# utils/file_cleanup.py
"""
File system cleanup utilities for The Basilisk Protocol.

Provides functions to clean up temporary files and Python cache directories.
"""

import os
import shutil
from typing import List, Set


def clean_pycache(directory: str = ".") -> None:
    """
    Recursively delete all __pycache__ folders in the given directory.
    
    Args:
        directory: Root directory to start cleaning from (default: current directory)
    """
    cleaned_paths: List[str] = []
    
    for root, dirs, files in os.walk(directory):
        # Skip virtual environment directories
        if 'venv' in root or '.venv' in root or 'env' in root:
            continue
            
        for d in dirs:
            if d == "__pycache__":
                full_path = os.path.join(root, d)
                try:
                    shutil.rmtree(full_path)
                    cleaned_paths.append(full_path)
                except PermissionError:
                    print(f"Permission denied: {full_path}")
                except Exception as e:
                    print(f"Error removing {full_path}: {e}")
    
    if cleaned_paths:
        print(f"Cleaned {len(cleaned_paths)} __pycache__ directories")


def clean_temp_files(
    directory: str = ".", 
    extensions: List[str] = None,
    skip_dirs: Set[str] = None
) -> None:
    """
    Remove temporary files with specified extensions.
    
    Args:
        directory: Root directory to clean
        extensions: List of file extensions to remove (e.g., ['.tmp', '.log'])
        skip_dirs: Set of directory names to skip
    """
    if extensions is None:
        extensions = ['.tmp', '.log', '.pyc', '.pyo']
    
    if skip_dirs is None:
        skip_dirs = {'venv', '.venv', 'env', '.git', 'node_modules'}
    
    removed_count = 0
    removed_size = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip specified directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    removed_count += 1
                    removed_size += file_size
                except Exception as e:
                    print(f"Error removing {file}: {e}")
    
    if removed_count:
        size_mb = removed_size / (1024 * 1024)
        print(f"Removed {removed_count} temporary files ({size_mb:.2f} MB)")


def get_directory_size(directory: str) -> int:
    """
    Calculate the total size of a directory in bytes.
    
    Args:
        directory: Path to directory
        
    Returns:
        Total size in bytes
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except:
                pass
    return total_size
# SPYHVER-48: WAITING
