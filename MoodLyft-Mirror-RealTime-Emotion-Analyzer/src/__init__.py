"""
MoodLyft Mirror - Source Package
Real-Time Emotion Analyzer with Modern UI

This package contains all the core modules for the MoodLyft Mirror application.
"""

__version__ = "1.0.0"
__author__ = "MoodLyft Team"

# Import main classes for easy access
from .emotion_detector import EmotionAnalyzer, SimpleFER
from .animation import AnimationManager
from .ui_elements import ModernUIElements
from .tts_manager import TTSManager, EmotionFeedbackManager
from .utils import load_fonts, get_system_info

__all__ = [
    'EmotionAnalyzer',
    'SimpleFER', 
    'AnimationManager',
    'ModernUIElements',
    'TTSManager',
    'EmotionFeedbackManager',
    'load_fonts',
    'get_system_info'
] 