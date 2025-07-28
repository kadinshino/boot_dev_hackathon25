# utils/__init__.py
"""
Utility modules for The Basilisk Protocol.

This package contains reusable utility functions for file operations,
text processing, logging, and performance monitoring.
"""

from .file_cleanup import clean_pycache, clean_temp_files
from .text_utils import wrap_text, truncate_text, sanitize_input
from .logging import logger, setup_logging
from .performance import PerformanceMonitor

__all__ = [
    'clean_pycache',
    'clean_temp_files',
    'wrap_text',
    'truncate_text',
    'sanitize_input',
    'logger',
    'setup_logging',
    'PerformanceMonitor'
]



# utils/performance.py
"""
Performance monitoring utilities for The Basilisk Protocol.

Provides tools for measuring and optimizing game performance.
"""

import time
import statistics
from typing import Dict, List, Optional, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class TimingData:
    """Stores timing information for a measured operation."""
    name: str
    times: List[float] = field(default_factory=list)
    
    @property
    def count(self) -> int:
        """Number of measurements."""
        return len(self.times)
    
    @property
    def total(self) -> float:
        """Total time spent."""
        return sum(self.times)
    
    @property
    def average(self) -> float:
        """Average time per call."""
        return statistics.mean(self.times) if self.times else 0
    
    @property
    def median(self) -> float:
        """Median time per call."""
        return statistics.median(self.times) if self.times else 0
    
    @property
    def min(self) -> float:
        """Minimum time recorded."""
        return min(self.times) if self.times else 0
    
    @property
    def max(self) -> float:
        """Maximum time recorded."""
        return max(self.times) if self.times else 0
    
    @property
    def std_dev(self) -> float:
        """Standard deviation of times."""
        return statistics.stdev(self.times) if len(self.times) > 1 else 0


class PerformanceMonitor:
    """
    Simple performance monitoring for game optimization.
    
    Usage:
        monitor = PerformanceMonitor()
        
        with monitor.measure('render'):
            # code to measure
            pass
            
        print(monitor.report())
    """
    
    def __init__(self, enabled: bool = True):
        """
        Initialize the performance monitor.
        
        Args:
            enabled: If False, monitoring is disabled (no overhead)
        """
        self.enabled = enabled
        self.timings: Dict[str, TimingData] = {}
        self.start_time = time.perf_counter()
    
    @contextmanager
    def measure(self, name: str):
        """
        Context manager to measure execution time.
        
        Args:
            name: Name of the operation being measured
        """
        if not self.enabled:
            yield
            return
            
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self._record_timing(name, duration)
    
    def measure_function(self, name: Optional[str] = None) -> Callable:
        """
        Decorator to measure function execution time.
        
        Args:
            name: Name for the measurement (defaults to function name)
            
        Usage:
            @monitor.measure_function()
            def my_function():
                pass
        """
        def decorator(func: Callable) -> Callable:
            measurement_name = name or func.__name__
            
            def wrapper(*args, **kwargs):
                with self.measure(measurement_name):
                    return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
    
    def _record_timing(self, name: str, duration: float) -> None:
        """Record a timing measurement."""
        if name not in self.timings:
            self.timings[name] = TimingData(name)
        
        self.timings[name].times.append(duration)
    
    def get_timing(self, name: str) -> Optional[TimingData]:
        """Get timing data for a specific operation."""
        return self.timings.get(name)
    
    def reset(self, name: Optional[str] = None) -> None:
        """
        Reset measurements.
        
        Args:
            name: If provided, reset only this measurement
        """
        if name:
            if name in self.timings:
                self.timings[name].times.clear()
        else:
            self.timings.clear()
            self.start_time = time.perf_counter()
    
    def report(self, sort_by: str = 'total', top_n: Optional[int] = None) -> str:
        """
        Generate a performance report.
        
        Args:
            sort_by: Sort criterion ('total', 'average', 'count', 'max')
            top_n: Show only top N entries
            
        Returns:
            Formatted performance report
        """
        if not self.timings:
            return "No performance data collected."
        
        # Sort timings
        sorted_timings = sorted(
            self.timings.values(),
            key=lambda t: getattr(t, sort_by),
            reverse=True
        )
        
        if top_n:
            sorted_timings = sorted_timings[:top_n]
        
        # Build report
        lines = [
            f"Performance Report (sorted by {sort_by}):",
            f"Total runtime: {time.perf_counter() - self.start_time:.2f}s",
            "-" * 80
        ]
        
        # Header
        lines.append(
            f"{'Operation':<30} {'Count':>8} {'Total':>10} {'Average':>10} "
            f"{'Min':>10} {'Max':>10} {'Std Dev':>10}"
        )
        lines.append("-" * 80)
        
        # Data rows
        for timing in sorted_timings:
            lines.append(
                f"{timing.name:<30} {timing.count:>8} "
                f"{timing.total*1000:>10.2f} {timing.average*1000:>10.2f} "
                f"{timing.min*1000:>10.2f} {timing.max*1000:>10.2f} "
                f"{timing.std_dev*1000:>10.2f}"
            )
        
        lines.append("-" * 80)
        lines.append("All times in milliseconds")
        
        return '\n'.join(lines)
    
    def get_fps_counter(self, window_size: int = 60) -> 'FPSCounter':
        """
        Get an FPS counter instance.
        
        Args:
            window_size: Number of frames to average over
            
        Returns:
            FPS counter instance
        """
        return FPSCounter(window_size)


class FPSCounter:
    """
    Tracks frames per second with a rolling average.
    """
    
    def __init__(self, window_size: int = 60):
        """
        Initialize FPS counter.
        
        Args:
            window_size: Number of frames to average over
        """
        self.window_size = window_size
        self.frame_times: List[float] = []
        self.last_time = time.perf_counter()
    
    def tick(self) -> None:
        """Call once per frame to update FPS calculation."""
        current_time = time.perf_counter()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
    
    @property
    def fps(self) -> float:
        """Current FPS based on rolling average."""
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = statistics.mean(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    @property
    def frame_time(self) -> float:
        """Average frame time in milliseconds."""
        if not self.frame_times:
            return 0.0
        
        return statistics.mean(self.frame_times) * 1000
    
    def __str__(self) -> str:
        """String representation showing FPS and frame time."""
        return f"FPS: {self.fps:.1f} ({self.frame_time:.1f}ms)"


# Global performance monitor instance
monitor = PerformanceMonitor()
# SPYHVER-47: SIGNAL'S
