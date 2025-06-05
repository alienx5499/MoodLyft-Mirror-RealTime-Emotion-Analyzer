"""
Configuration file for MoodLyft-Mirror
Adjust these settings based on your hardware capabilities and preferences
"""

class PerformanceConfig:
    """Performance-related configuration options"""
    
    # Emotion detection frequency (process every N frames)
    # Higher values = better performance, lower accuracy
    # Lower values = better accuracy, lower performance
    EMOTION_SKIP_FRAMES = 3  # Default: 3 (good balance)
    
    # Camera settings
    CAMERA_WIDTH = 1280
    CAMERA_HEIGHT = 720
    CAMERA_FPS = 30
    
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
    TTS_RATE = 160  # Words per minute
    TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)
    
    # Timing
    COMPLIMENT_COOLDOWN = 8  # Seconds between compliments
    NO_FACE_COOLDOWN = 5  # Seconds between "no face" messages
    
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