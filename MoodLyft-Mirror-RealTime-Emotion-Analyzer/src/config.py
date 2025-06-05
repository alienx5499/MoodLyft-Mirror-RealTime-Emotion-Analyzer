"""
Configuration file for MoodLyft-Mirror
Adjust these settings based on your hardware capabilities and preferences
"""

import os
from typing import Dict, List, Tuple

########################################
# DIRECTORIES FOR OUTPUT
########################################
VIDEOS_DIR = "Output/Videos"
SCREENSHOTS_DIR = "Output/Screenshots"

# Ensure directories exist
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

########################################
# PERFORMANCE SETTINGS
########################################
# Frame processing optimization
EMOTION_SKIP_FRAMES = 8  # Process emotion every N frames for better FPS
DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480
DEFAULT_FPS = 30

# Cooldown timings (in seconds)
COMPLIMENT_COOLDOWN = 8
NO_FACE_COOLDOWN = 5

########################################
# ENHANCED EMOTION DATA
########################################
COMPLIMENTS = {
    "happy": [
        "Your radiant smile lights up the entire room! ✨",
        "That genuine happiness is absolutely contagious! 🌟",
        "You have such a warm, inviting presence! 💫",
        "Your joy creates beautiful ripples of positivity! 🌈",
        "Keep shining with that magnificent energy! ⭐"
    ],
    "neutral": [
        "Your calm presence brings such peaceful energy! 🧘",
        "There's incredible strength in your composure! 💪",
        "Your steady energy is truly admirable! 🌿",
        "You bring perfect balance wherever you go! ⚖️",
        "Your mindful presence is deeply appreciated! 🕯️"
    ],
    "sad": [
        "You're so much stronger than you realize! 💪",
        "Every storm passes - brighter days ahead! 🌅",
        "Your resilience is truly inspiring to witness! 🦋",
        "Better days are coming - believe in yourself! 🌱",
        "You're never alone in this beautiful journey! 🤝"
    ],
    "angry": [
        "Channel that powerful energy into positive change! ⚡",
        "Your passion can truly move mountains! 🏔️",
        "Transform that fire into unstoppable motivation! 🔥",
        "Your intensity can spark absolutely amazing things! 💥",
        "Use that incredible power to achieve greatness! 🚀"
    ],
    "surprise": [
        "Your sense of wonder is so refreshing! 🌺",
        "Stay curious and keep exploring life! 🔍",
        "Life is overflowing with amazing discoveries! 🗺️",
        "Your enthusiasm is beautifully infectious! 🎉",
        "Keep embracing new and exciting experiences! 🎭"
    ],
    "fear": [
        "Courage isn't fearlessness - it's facing fear head-on! 🦸",
        "You're so much braver than you believe! 🛡️",
        "Every step forward conquers fear completely! 👣",
        "Your strength shines through any uncertainty! ✨",
        "Fear is temporary - your courage is permanent! 💎"
    ],
    "disgust": [
        "Your standards show incredible self-respect! 👑",
        "Trust your instincts - they serve you perfectly! 🧭",
        "Your boundaries protect your inner peace! 🛡️",
        "Standing firm shows true inner strength! 🌳",
        "Your authenticity is genuinely powerful! 💯"
    ]
}

########################################
# ENHANCED COLOR SCHEMES
########################################
COLOR_MAP = {
    "happy":   {"primary": (255, 215, 0), "secondary": (255, 255, 224), "accent": (255, 140, 0)},
    "neutral": {"primary": (169, 169, 169), "secondary": (211, 211, 211), "accent": (105, 105, 105)},
    "sad":     {"primary": (138, 43, 226), "secondary": (221, 160, 221), "accent": (75, 0, 130)},
    "angry":   {"primary": (220, 20, 60), "secondary": (255, 182, 193), "accent": (139, 0, 0)},
    "surprise":{"primary": (255, 165, 0), "secondary": (255, 228, 181), "accent": (255, 69, 0)},
    "fear":    {"primary": (72, 61, 139), "secondary": (230, 230, 250), "accent": (25, 25, 112)},
    "disgust": {"primary": (50, 205, 50), "secondary": (144, 238, 144), "accent": (0, 128, 0)}
}

# Enhanced emoji set with variations
EMOJIS = {
    "happy": ["😊", "😁", "😄", "🥰", "😍"],
    "neutral": ["😌", "😐", "🙂", "😶", "😏"],
    "sad": ["🥺", "😢", "😔", "😞", "🙁"],
    "angry": ["😤", "😠", "😡", "🤬", "😾"],
    "surprise": ["😲", "😮", "🤯", "😱", "🙀"],
    "fear": ["😨", "😰", "😱", "🫣", "😧"],
    "disgust": ["😖", "🤢", "😬", "🙄", "😒"]
}

########################################
# FONT CONFIGURATIONS
########################################
FONT_PATHS = {
    "Windows": {
        'default': ["arial.ttf", "calibri.ttf", "segoeui.ttf"],
        'fancy': ["arialbd.ttf", "calibrib.ttf", "segoeuib.ttf"],
        'mono': ["consolas.ttf", "cour.ttf"]
    },
    "Darwin": {
        'default': ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Arial.ttf"],
        'fancy': ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"],
        'mono': ["/System/Library/Fonts/Monaco.ttf", "/System/Library/Fonts/Courier New.ttf"]
    },
    "Linux": {
        'default': ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
        'fancy': ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        'mono': ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    }
}

########################################
# TTS SETTINGS
########################################
TTS_RATE = 160  # Speech rate
TTS_VOLUME = 0.9  # Speech volume
TTS_PREFERRED_VOICES = ['en_US', 'female', 'english']

########################################
# UI SETTINGS
########################################
UI_PANEL_HEIGHT = 80
UI_PANEL_PADDING = 10
UI_ROUNDED_CORNER_RADIUS = 20
UI_CONFIDENCE_BAR_HEIGHT = 8
UI_BORDER_THICKNESS = 3

# Animation settings
ANIMATION_DURATIONS = {
    'pulse': 2.0,
    'breath': 4.0,
    'wave': 3.0,
    'float': 3.0
}

ANIMATION_INTENSITIES = {
    'pulse': 1.0,
    'breath': 0.7,
    'glow': 0.6,
    'float': 10  # pixels
}

class PerformanceConfig:
    """Performance-related configuration options"""
    
    # Emotion detection frequency (process every N frames)
    # Higher values = better performance, lower accuracy
    # Lower values = better accuracy, lower performance
    EMOTION_SKIP_FRAMES = EMOTION_SKIP_FRAMES
    
    # Camera settings
    CAMERA_WIDTH = DEFAULT_CAMERA_WIDTH
    CAMERA_HEIGHT = DEFAULT_CAMERA_HEIGHT
    CAMERA_FPS = DEFAULT_FPS
    
    # Frame processing
    ENABLE_THREADING = True  # Enable threaded TTS
    BUFFER_SIZE = 1  # Camera buffer size (lower = less latency)
    
    # Memory optimization
    EMOTION_HISTORY_SIZE = 30  # Number of emotion readings to keep
    FPS_HISTORY_SIZE = 30  # Number of FPS readings for averaging

class VisualConfig:
    """Visual and UI configuration options"""
    
    # Animation settings
    ENABLE_ANIMATIONS = True
    ANIMATION_SPEED = 1.0  # Multiplier for animation speed
    PULSE_DURATION = 2.0  # Duration of pulsing animations in seconds
    
    # Color transition
    COLOR_TRANSITION_SPEED = 0.05  # How fast emotions colors transition
    
    # UI elements
    ENABLE_GLASSMORPHISM = True  # Modern glass-like effects
    ENABLE_GLOW_EFFECTS = True
    ENABLE_PARTICLE_EFFECTS = False  # Experimental
    
    # Text and fonts
    FONT_SIZE_MULTIPLIER = 1.0  # Scale all fonts
    ENABLE_TEXT_SHADOWS = True
    
    # Opacity and blending
    BACKGROUND_OPACITY = 0.15  # Background overlay opacity
    UI_PANEL_OPACITY = 0.7  # Top panel opacity
    COMPLIMENT_BACKGROUND_OPACITY = 0.8

class AudioConfig:
    """Audio and TTS configuration"""
    
    # Text-to-speech
    TTS_RATE = TTS_RATE
    TTS_VOLUME = TTS_VOLUME
    
    # Timing
    COMPLIMENT_COOLDOWN = COMPLIMENT_COOLDOWN
    NO_FACE_COOLDOWN = NO_FACE_COOLDOWN
    
    # Voice preferences
    PREFER_FEMALE_VOICE = True
    VOICE_LANGUAGE = "en_US"

class EmotionConfig:
    """Emotion detection and feedback configuration"""
    
    # Confidence thresholds
    MIN_CONFIDENCE_FOR_COMPLIMENT = 0.7  # Minimum confidence to trigger compliment
    MIN_CONFIDENCE_FOR_DISPLAY = 0.3  # Minimum confidence to display emotion
    
    # Emotion smoothing
    ENABLE_EMOTION_SMOOTHING = True
    SMOOTHING_FACTOR = 0.3  # How much to smooth emotion transitions
    
    # Advanced options
    USE_MTCNN = True  # More accurate face detection (slower)
    ENABLE_EMOTION_HISTORY_GRAPH = True

class DeveloperConfig:
    """Developer and debugging options"""
    
    # Logging
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_PERFORMANCE_METRICS = False
    
    # Debugging
    SHOW_DEBUG_INFO = False  # Show technical info on screen
    SAVE_DEBUG_FRAMES = False  # Save processed frames for analysis
    
    # Experimental features
    ENABLE_EXPERIMENTAL_FEATURES = False

# Hardware presets for easy configuration
class HardwarePresets:
    """Pre-configured settings for different hardware capabilities"""
    
    @staticmethod
    def high_performance():
        """Settings for high-end hardware"""
        PerformanceConfig.EMOTION_SKIP_FRAMES = 1
        PerformanceConfig.CAMERA_FPS = 30
        VisualConfig.ENABLE_ANIMATIONS = True
        VisualConfig.ENABLE_GLASSMORPHISM = True
        VisualConfig.ENABLE_GLOW_EFFECTS = True
        VisualConfig.ENABLE_PARTICLE_EFFECTS = True
    
    @staticmethod
    def balanced():
        """Balanced settings for most hardware"""
        PerformanceConfig.EMOTION_SKIP_FRAMES = 3
        PerformanceConfig.CAMERA_FPS = 30
        VisualConfig.ENABLE_ANIMATIONS = True
        VisualConfig.ENABLE_GLASSMORPHISM = True
        VisualConfig.ENABLE_GLOW_EFFECTS = True
        VisualConfig.ENABLE_PARTICLE_EFFECTS = False
    
    @staticmethod
    def performance_mode():
        """Settings optimized for older hardware"""
        PerformanceConfig.EMOTION_SKIP_FRAMES = 5
        PerformanceConfig.CAMERA_FPS = 20
        PerformanceConfig.CAMERA_WIDTH = 640
        PerformanceConfig.CAMERA_HEIGHT = 480
        VisualConfig.ENABLE_ANIMATIONS = False
        VisualConfig.ENABLE_GLASSMORPHISM = False
        VisualConfig.ENABLE_GLOW_EFFECTS = False
        VisualConfig.ENABLE_PARTICLE_EFFECTS = False
    
    @staticmethod
    def battery_saver():
        """Settings for laptops/mobile devices"""
        PerformanceConfig.EMOTION_SKIP_FRAMES = 7
        PerformanceConfig.CAMERA_FPS = 15
        VisualConfig.ENABLE_ANIMATIONS = False
        VisualConfig.ANIMATION_SPEED = 0.5
        AudioConfig.COMPLIMENT_COOLDOWN = 15

# Auto-detect and apply appropriate preset
def auto_configure():
    """Automatically configure based on system capabilities"""
    import psutil
    import platform
    
    # Get system info
    cpu_count = psutil.cpu_count()
    memory_gb = psutil.virtual_memory().total / (1024**3)
    system = platform.system()
    
    # Apply preset based on system capabilities
    if cpu_count >= 8 and memory_gb >= 16:
        print("🚀 High-performance system detected - applying high-performance preset")
        HardwarePresets.high_performance()
    elif cpu_count >= 4 and memory_gb >= 8:
        print("⚖️ Balanced system detected - applying balanced preset")
        HardwarePresets.balanced()
    else:
        print("🔋 Lower-end system detected - applying performance preset")
        HardwarePresets.performance_mode()

# Apply auto-configuration by default
if __name__ != "__main__":
    try:
        auto_configure()
    except ImportError:
        print("⚖️ Unable to detect system specs - using balanced preset")
        HardwarePresets.balanced() 