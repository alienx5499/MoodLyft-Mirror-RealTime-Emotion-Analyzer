import cv2
import numpy as np
import random
from typing import Tuple, Dict, Optional, List
from PIL import Image, ImageDraw, ImageFont
from collections import deque

from .animation import AnimationManager
from .config import COLOR_MAP, EMOJIS, UI_BORDER_THICKNESS, UI_CONFIDENCE_BAR_HEIGHT


class ModernUIElements:
    """Handles all modern UI drawing and visual effects"""
    
    def __init__(self):
        self.animation_manager = AnimationManager()
        self.particle_systems = []
    
    @staticmethod
    def create_glassmorphism_background(width: int, height: int, 
                                      base_color: Tuple[int, int, int], 
                                      opacity: float = 0.1) -> np.ndarray:
        """Creates a modern glassmorphism background effect"""
        background = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create gradient with noise
        for y in range(height):
            for x in range(width):
                # Add some noise for texture
                noise = np.random.normal(0, 10)
                alpha = (y / height) * 0.3 + 0.7
                color = tuple(int(base_color[i] * alpha + noise) for i in range(3))
                color = tuple(max(0, min(255, c)) for c in color)
                background[y, x] = color
        
        return background
    
    def create_animated_border(self, img: np.ndarray, x: int, y: int, 
                             w: int, h: int, color: Tuple[int, int, int], 
                             thickness: int = UI_BORDER_THICKNESS, style: str = "glow") -> None:
        """Creates beautiful animated borders with multiple styles"""
        if style == "glow":
            # Smooth breathing glow effect
            breath = self.animation_manager.create_breath_animation(3.0)
            pulse = self.animation_manager.create_pulse_animation(2.5, 0.6)
            intensity = 0.4 + 0.6 * breath + 0.2 * pulse
            
            # Multi-layer glow effect
            for i in range(thickness * 2):
                layer_intensity = intensity * (1.0 - (i / (thickness * 2))) ** 0.5
                border_color = tuple(int(c * layer_intensity) for c in color)
                offset = i // 2
                cv2.rectangle(img, (x - offset, y - offset), (x + w + offset, y + h + offset), border_color, 1)
        
        elif style == "wave":
            # Flowing wave border
            for i in range(thickness):
                wave = self.animation_manager.create_wave_animation(x + i, y + i, i * 0.1, 0.8)
                intensity = 0.3 + 0.7 * wave
                border_color = tuple(int(c * intensity) for c in color)
                cv2.rectangle(img, (x - i, y - i), (x + w + i, y + h + i), border_color, 1)
        
        elif style == "pulse":
            # Sharp pulsing effect
            pulse = self.animation_manager.create_pulse_animation(1.5, 1.2)
            eased_pulse = self.animation_manager.ease_out_back(pulse)
            
            for i in range(thickness):
                intensity = eased_pulse * (1.0 - (i / thickness))
                border_color = tuple(int(c * intensity) for c in color)
                cv2.rectangle(img, (x - i, y - i), (x + w + i, y + h + i), border_color, 2)
    
    def draw_modern_rounded_rect(self, img: np.ndarray, x: int, y: int, 
                               w: int, h: int, radius: int, 
                               color: Tuple[int, int, int], 
                               border_color: Optional[Tuple[int, int, int]] = None,
                               alpha: float = 0.8) -> None:
        """Draws a modern rounded rectangle with glassmorphism effect"""
        # Create overlay for alpha blending
        overlay = img.copy()
        
        # Draw filled rounded rectangle
        cv2.rectangle(overlay, (x + radius, y), (x + w - radius, y + h), color, -1)
        cv2.rectangle(overlay, (x, y + radius), (x + w, y + h - radius), color, -1)
        
        # Corner circles
        cv2.circle(overlay, (x + radius, y + radius), radius, color, -1)
        cv2.circle(overlay, (x + w - radius, y + radius), radius, color, -1)
        cv2.circle(overlay, (x + radius, y + h - radius), radius, color, -1)
        cv2.circle(overlay, (x + w - radius, y + h - radius), radius, color, -1)
        
        # Blend with original image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        # Add border if specified
        if border_color:
            self.create_animated_border(img, x, y, w, h, border_color)
    
    def draw_confidence_bar(self, img: np.ndarray, x: int, y: int, 
                          width: int, height: int, confidence: float, 
                          color: Tuple[int, int, int], animated: bool = True) -> None:
        """Draws a beautiful animated confidence bar with gradient effects"""
        # Enhanced background with subtle gradient
        bg_gradient = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(width):
            intensity = 20 + int(10 * (i / width))
            bg_gradient[:, i] = [intensity, intensity, intensity]
        
        # Apply background
        img[y:y+height, x:x+width] = bg_gradient
        
        # Animated fill with smooth transitions
        fill_width = int(width * confidence)
        
        if animated:
            # Breathing animation for subtle movement
            breath = self.animation_manager.create_breath_animation(4.0)
            pulse = self.animation_manager.create_pulse_animation(2.0, 0.4)
            intensity_mult = 0.7 + 0.2 * breath + 0.1 * pulse
        else:
            intensity_mult = 0.8
        
        if fill_width > 0:
            # Create gradient fill
            fill_gradient = np.zeros((height, fill_width, 3), dtype=np.uint8)
            
            for i in range(fill_width):
                # Gradient from darker to lighter
                gradient_progress = i / fill_width
                base_intensity = 0.6 + 0.4 * gradient_progress
                
                if animated:
                    # Add wave effect for more dynamic look
                    wave = self.animation_manager.create_wave_animation(x + i, y, 0, 0.5)
                    wave_intensity = 0.9 + 0.1 * wave
                    final_intensity = base_intensity * intensity_mult * wave_intensity
                else:
                    final_intensity = base_intensity * intensity_mult
                
                animated_color = tuple(int(c * final_intensity) for c in color)
                fill_gradient[:, i] = animated_color[::-1]  # BGR format
            
            # Apply gradient fill
            img[y:y+height, x:x+fill_width] = fill_gradient
            
            # Add highlight line at the top
            highlight_color = tuple(min(255, int(c * 1.3)) for c in color)
            cv2.line(img, (x, y), (x + fill_width, y), highlight_color[::-1], 1)
        
        # Enhanced text with shadow
        text = f"{confidence:.0%}"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        
        # Text shadow
        cv2.putText(img, text, (text_x + 1, text_y + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)
        # Main text
        cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
    
    def draw_enhanced_emotion_label(self, overlay: np.ndarray, emotion: str, confidence: float,
                                   x: int, y: int, w_box: int, color_scheme: Dict, fonts: Dict) -> None:
        """Draw enhanced emotion label with modern styling"""
        # Convert to PIL for better text rendering
        pil_img = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        
        # Select random emoji from emotion set
        emoji = random.choice(EMOJIS.get(emotion, ["😐"]))
        label_text = f"{emoji} {emotion.title()}"
        confidence_text = f"{confidence:.1%}"
        
        # Use fancy font
        font = fonts.get('fancy', ImageFont.load_default())
        small_font = fonts.get('default', ImageFont.load_default())
        
        # Calculate text dimensions
        label_bbox = draw.textbbox((0, 0), label_text, font=font)
        conf_bbox = draw.textbbox((0, 0), confidence_text, font=small_font)
        
        label_w = label_bbox[2] - label_bbox[0]
        label_h = label_bbox[3] - label_bbox[1]
        conf_w = conf_bbox[2] - conf_bbox[0]
        conf_h = conf_bbox[3] - conf_bbox[1]
        
        # Position above the face
        total_height = label_h + conf_h + 10
        text_x = x + (w_box - max(label_w, conf_w)) // 2
        text_y = y - total_height - 20
        
        # Draw glassmorphism background
        padding = 15
        bg_x = text_x - padding
        bg_y = text_y - padding
        bg_w = max(label_w, conf_w) + 2 * padding
        bg_h = total_height + 2 * padding
        
        # Create rounded rectangle with gradient
        bg_color = tuple(int(c * 0.8) for c in color_scheme['primary'])
        draw.rounded_rectangle(
            [bg_x, bg_y, bg_x + bg_w, bg_y + bg_h],
            radius=12, fill=(*bg_color, 180)
        )
        
        # Draw text with shadow effect
        shadow_offset = 2
        # Shadow
        draw.text((text_x + shadow_offset, text_y + shadow_offset), label_text, 
                 font=font, fill=(0, 0, 0, 128))
        # Main text
        draw.text((text_x, text_y), label_text, font=font, fill=(255, 255, 255, 255))
        
        # Confidence text
        conf_x = text_x + (label_w - conf_w) // 2
        conf_y = text_y + label_h + 5
        draw.text((conf_x + shadow_offset, conf_y + shadow_offset), confidence_text,
                 font=small_font, fill=(0, 0, 0, 128))
        draw.text((conf_x, conf_y), confidence_text, font=small_font, fill=(255, 255, 255, 255))
        
        # Convert back to OpenCV
        overlay[:] = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def draw_emotion_history_graph(self, overlay: np.ndarray, x: int, y: int, 
                                  width: int, height: int, emotion_history: deque) -> None:
        """Draw an enhanced animated emotion history graph"""
        if len(emotion_history) < 2:
            return
        
        # Animated background with breathing effect
        breath = self.animation_manager.create_breath_animation(4.0)
        bg_intensity = int(30 + 10 * breath)
        cv2.rectangle(overlay, (x, y), (x + width, y + height), 
                     (bg_intensity, bg_intensity, bg_intensity), -1)
        
        # Add subtle border
        border_pulse = self.animation_manager.create_pulse_animation(3.0, 0.5)
        border_color = (60 + int(20 * border_pulse), 60 + int(20 * border_pulse), 60 + int(20 * border_pulse))
        cv2.rectangle(overlay, (x, y), (x + width, y + height), border_color, 1)
        
        # Plot animated points with emotion colors
        points = []
        colors = []
        for i, entry in enumerate(emotion_history):
            px = x + int((i / len(emotion_history)) * width)
            py = y + height - int(entry['confidence'] * height)
            points.append((px, py))
            
            # Get emotion color
            emotion_color = COLOR_MAP.get(entry['emotion'], COLOR_MAP['neutral'])['primary']
            colors.append(emotion_color)
        
        # Draw flowing lines with gradient effect
        for i in range(1, len(points)):
            # Animate the line thickness based on time and position
            wave = self.animation_manager.create_wave_animation(points[i][0], points[i][1], i * 0.1, 0.3)
            thickness = max(1, int(2 + wave))
            
            # Use color of current point
            line_color = colors[i]
            cv2.line(overlay, points[i-1], points[i], line_color, thickness)
        
        # Draw animated point markers
        for i, (point, color) in enumerate(zip(points, colors)):
            # Animate point size
            point_pulse = self.animation_manager.create_pulse_animation(2.0 + i * 0.1, 0.4)
            radius = max(2, int(3 + point_pulse))
            cv2.circle(overlay, point, radius, color, -1)
            
            # Add subtle glow around recent points
            if i >= len(points) - 5:  # Last 5 points
                glow_radius = radius + 2
                glow_color = tuple(int(c * 0.3) for c in color)
                cv2.circle(overlay, point, glow_radius, glow_color, 1)
    
    def draw_enhanced_compliment(self, overlay: np.ndarray, w: int, h: int, 
                               compliment_text: str, fonts: Dict) -> None:
        """Draw compliment with enhanced styling"""
        if not compliment_text:
            return
            
        # Convert to PIL for better text handling
        pil_img = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        
        # Use fancy font
        font = fonts.get('fancy', ImageFont.load_default())
        
        # Calculate text dimensions
        lines = compliment_text.split('\n')
        line_heights = []
        line_widths = []
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_widths.append(bbox[2] - bbox[0])
            line_heights.append(bbox[3] - bbox[1])
        
        max_width = max(line_widths)
        total_height = sum(line_heights) + (len(lines) - 1) * 5
        
        # Position
        x = (w - max_width) // 2
        y = h - total_height - 80
        
        # Enhanced animated background with multiple effects
        breath = self.animation_manager.create_breath_animation(5.0)
        pulse = self.animation_manager.create_pulse_animation(3.0, 0.4)
        wave = self.animation_manager.create_wave_animation(x, y, 0, 0.2)
        
        # Combine animations for richer effect
        bg_alpha = int(150 + 30 * breath + 20 * pulse + 10 * wave)
        
        # Add floating effect to compliment position
        floating_y = self.animation_manager.create_floating_animation(y, 5, 4.0)
        
        # Draw enhanced glassmorphism background with floating effect
        padding = 20
        bg_y = floating_y - padding
        
        # Multi-layer background for depth
        for layer in range(3):
            layer_alpha = bg_alpha // (layer + 1)
            layer_radius = 25 + layer * 2
            layer_offset = layer * 2
            
            draw.rounded_rectangle(
                [x - padding - layer_offset, bg_y - layer_offset, 
                 x + max_width + padding + layer_offset, floating_y + total_height + padding + layer_offset],
                radius=layer_radius, fill=(30 + layer * 10, 35 + layer * 10, 50 + layer * 10, layer_alpha)
            )
        
        # Draw text lines with floating effect and enhanced shadows
        current_y = floating_y
        for i, line in enumerate(lines):
            line_x = x + (max_width - line_widths[i]) // 2
            
            # Animated text glow
            text_pulse = self.animation_manager.create_pulse_animation(2.5 + i * 0.2, 0.3)
            text_alpha = int(255 * (0.9 + 0.1 * text_pulse))
            
            # Enhanced shadow with multiple layers
            for shadow_offset in range(3, 0, -1):
                shadow_alpha = 40 * (4 - shadow_offset)
                draw.text((line_x + shadow_offset, current_y + shadow_offset), line, 
                         font=font, fill=(0, 0, 0, shadow_alpha))
            
            # Main text with animated glow
            draw.text((line_x, current_y), line, font=font, fill=(255, 255, 255, text_alpha))
            current_y += line_heights[i] + 5
        
        # Convert back
        overlay[:] = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def draw_fps_indicator(self, overlay: np.ndarray, fps: float, x: int, y: int) -> None:
        """Draw FPS indicator with color coding"""
        fps_color = (0, 255, 0) if fps > 25 else (255, 255, 0) if fps > 15 else (255, 0, 0)
        cv2.putText(overlay, f"FPS: {fps:.1f}", (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, fps_color, 2)
    
    def draw_app_title(self, overlay: np.ndarray, x: int, y: int) -> None:
        """Draw animated app title"""
        # Add subtle glow effect to title
        title_pulse = self.animation_manager.create_pulse_animation(4.0, 0.3)
        title_alpha = int(255 * (0.8 + 0.2 * title_pulse))
        
        cv2.putText(overlay, "MoodLyft Mirror", (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(overlay, "Real-time Emotion Analysis", (x, y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1) 