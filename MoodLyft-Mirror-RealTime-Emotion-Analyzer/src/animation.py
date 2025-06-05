import math
import time
from typing import Tuple

from .config import ANIMATION_DURATIONS, ANIMATION_INTENSITIES


class AnimationManager:
    """Handles all animation calculations and effects"""
    
    def __init__(self):
        self.animations = {}
        self.start_time = time.time()
        self.animation_cache = {}
    
    def ease_in_out_cubic(self, t: float) -> float:
        """Smooth easing function for animations"""
        return 3 * t * t - 2 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    
    def ease_out_elastic(self, t: float) -> float:
        """Elastic easing for bouncy animations"""
        if t == 0 or t == 1:
            return t
        return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1
    
    def ease_out_back(self, t: float) -> float:
        """Back easing for slight overshoot effect"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
    
    def create_pulse_animation(self, duration: float = None, intensity: float = None) -> float:
        """Creates a smooth pulsing animation with variable intensity"""
        if duration is None:
            duration = ANIMATION_DURATIONS['pulse']
        if intensity is None:
            intensity = ANIMATION_INTENSITIES['pulse']
            
        elapsed = (time.time() - self.start_time) % duration
        progress = elapsed / duration
        base_pulse = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
        # Apply easing for smoother pulse
        eased_pulse = self.ease_in_out_cubic(base_pulse)
        return 0.5 + (eased_pulse - 0.5) * intensity
    
    def create_breath_animation(self, duration: float = None) -> float:
        """Creates a breathing-like animation (slower, more organic)"""
        if duration is None:
            duration = ANIMATION_DURATIONS['breath']
            
        elapsed = (time.time() - self.start_time) % duration
        progress = elapsed / duration
        # Use cosine for smoother breathing effect
        intensity = ANIMATION_INTENSITIES['breath']
        return 0.3 + intensity * (1 + math.cos(progress * 2 * math.pi)) / 2
    
    def create_wave_animation(self, x: int, y: int, time_offset: float = 0, speed: float = 1.0) -> float:
        """Creates a wave animation based on position with speed control"""
        elapsed = (time.time() - self.start_time) * speed + time_offset
        wave = math.sin(elapsed + x * 0.008 + y * 0.008) * 0.5 + 0.5
        return self.ease_in_out_cubic(wave)
    
    def create_floating_animation(self, base_y: int, amplitude: int = None, duration: float = None) -> int:
        """Creates a floating effect for UI elements"""
        if amplitude is None:
            amplitude = ANIMATION_INTENSITIES['float']
        if duration is None:
            duration = ANIMATION_DURATIONS['float']
            
        elapsed = (time.time() - self.start_time) % duration
        progress = elapsed / duration
        offset = math.sin(progress * 2 * math.pi) * amplitude
        return base_y + int(offset)
    
    def animate_color_transition(self, from_color: Tuple[int, int, int], 
                               to_color: Tuple[int, int, int], progress: float) -> Tuple[int, int, int]:
        """Smoothly transitions between two colors with easing"""
        progress = max(0, min(1, progress))
        eased_progress = self.ease_in_out_cubic(progress)
        return tuple(int(from_color[i] + (to_color[i] - from_color[i]) * eased_progress) for i in range(3))
    
    def animate_scale(self, base_scale: float, progress: float, max_scale: float = 1.2) -> float:
        """Animate scale with bounce effect"""
        if progress <= 0:
            return base_scale
        elif progress >= 1:
            return base_scale
        else:
            bounce = self.ease_out_elastic(progress)
            return base_scale + (max_scale - base_scale) * bounce
    
    def create_ripple_effect(self, center_x: int, center_y: int, radius: float, max_radius: float = 100) -> float:
        """Creates expanding ripple animation"""
        elapsed = (time.time() - self.start_time) % 3.0  # 3 second cycle
        progress = elapsed / 3.0
        
        # Calculate distance-based intensity
        if radius > max_radius:
            return 0.0
        
        # Create expanding wave
        wave_progress = (progress * max_radius - radius) / max_radius
        if wave_progress < 0 or wave_progress > 1:
            return 0.0
        
        # Smooth falloff
        intensity = math.sin(wave_progress * math.pi) * (1 - wave_progress)
        return max(0, intensity)
    
    def create_glow_animation(self, base_intensity: float = 0.5, speed: float = 1.0) -> float:
        """Creates a soft glowing effect"""
        elapsed = (time.time() - self.start_time) * speed
        glow = base_intensity + ANIMATION_INTENSITIES['glow'] * math.sin(elapsed) * 0.5
        return max(0, min(1, glow))
    
    def create_sparkle_animation(self, x: int, y: int, frequency: float = 0.1) -> bool:
        """Creates random sparkle effects based on position and time"""
        # Use position and time to create pseudo-random sparkles
        seed = (x * 7 + y * 13) % 100
        time_factor = int((time.time() - self.start_time) * 10) % 100
        combined = (seed + time_factor) % 100
        return combined < (frequency * 100)
    
    def reset_time(self):
        """Reset animation start time"""
        self.start_time = time.time()
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since animation start"""
        return time.time() - self.start_time 