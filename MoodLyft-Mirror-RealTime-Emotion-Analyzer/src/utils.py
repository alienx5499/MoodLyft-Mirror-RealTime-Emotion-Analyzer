import os
import platform
import cv2
import numpy as np
from typing import Dict, Optional, Tuple
from PIL import ImageFont
import logging

from .config import FONT_PATHS


def get_system_info() -> Dict[str, str]:
    """Get comprehensive system information"""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'opencv_version': cv2.__version__
    }


def load_fonts(size: int = 24) -> Dict[str, ImageFont.ImageFont]:
    """Load system fonts with fallbacks"""
    fonts = {}
    system = platform.system()
    
    font_configs = FONT_PATHS.get(system, FONT_PATHS['Linux'])
    
    # Try to load fonts for each category
    for category, paths in font_configs.items():
        font_loaded = False
        for font_path in paths:
            try:
                if os.path.exists(font_path):
                    fonts[category] = ImageFont.truetype(font_path, size)
                    font_loaded = True
                    break
            except (OSError, IOError):
                continue
        
        # Fallback to default font if none loaded
        if not font_loaded:
            try:
                fonts[category] = ImageFont.load_default()
            except:
                fonts[category] = ImageFont.load_default()
    
    return fonts


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max"""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values"""
    return a + (b - a) * clamp(t, 0.0, 1.0)


def distance_2d(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two 2D points"""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def normalize_color(color: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Normalize RGB color values to 0-1 range"""
    return tuple(c / 255.0 for c in color)


def denormalize_color(color: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """Denormalize RGB color values from 0-1 to 0-255 range"""
    return tuple(int(c * 255) for c in color)


def format_time_elapsed(seconds: float) -> str:
    """Format elapsed time in a human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    return numerator / denominator if denominator != 0 else default


def create_directory_if_not_exists(directory: str) -> bool:
    """Create directory if it doesn't exist, return success status"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def get_border_style_for_emotion(emotion: str) -> str:
    """Get appropriate border animation style for emotion"""
    style_map = {
        "happy": "pulse",
        "surprise": "pulse", 
        "sad": "wave",
        "fear": "wave",
        "angry": "glow",
        "disgust": "glow",
        "neutral": "glow"
    }
    return style_map.get(emotion, "glow")


def format_confidence(confidence: float) -> str:
    """Format confidence as percentage string"""
    return f"{confidence:.1%}"


def format_fps(fps: float) -> str:
    """Format FPS for display"""
    return f"FPS: {fps:.1f}" 