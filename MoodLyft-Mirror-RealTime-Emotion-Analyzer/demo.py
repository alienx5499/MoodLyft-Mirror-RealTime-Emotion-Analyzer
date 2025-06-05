#!/usr/bin/env python3
"""
MoodLyft-Mirror Feature Demo
Showcases all the features and optimizations
"""

import cv2
import numpy as np
import time
import random
import math
from typing import Dict, List
from main import OptimizedEmotionDetector, COLOR_MAP, EMOJIS

class FeatureDemo:
    """Demonstrates specific features of the enhanced application"""
    
    def __init__(self):
        self.detector = OptimizedEmotionDetector()
        self.demo_features = [
            ("🎨 Glassmorphism UI", self.demo_glassmorphism),
            ("✨ Smooth Animations", self.demo_animations),
            ("📊 Emotion History", self.demo_emotion_history),
            ("🎭 Enhanced Face Detection", self.demo_face_detection),
            ("🔄 Performance Comparison", self.demo_performance),
            ("🎵 Audio Features", self.demo_audio),
        ]
        self.current_demo = 0
    
    def demo_glassmorphism(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate glassmorphism effects"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Create multiple glassmorphism panels
        panels = [
            {"x": 50, "y": 50, "w": 300, "h": 100, "color": (255, 100, 100)},
            {"x": 50, "y": 200, "w": 300, "h": 100, "color": (100, 255, 100)},
            {"x": 50, "y": 350, "w": 300, "h": 100, "color": (100, 100, 255)},
        ]
        
        for i, panel in enumerate(panels):
            alpha = 0.3 + 0.2 * math.sin(time.time() + i)
            self.detector.ui.draw_modern_rounded_rect(
                overlay, panel["x"], panel["y"], panel["w"], panel["h"], 20,
                color=panel["color"], alpha=alpha
            )
            
            # Add text
            text = f"Glassmorphism Panel {i+1}"
            cv2.putText(overlay, text, (panel["x"] + 20, panel["y"] + 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Add title
        cv2.putText(overlay, "🎨 Glassmorphism Effects Demo", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return overlay
    
    def demo_animations(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate smooth animations"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Pulsing circle
        pulse = self.detector.ui.animation_manager.create_pulse_animation()
        radius = int(50 + 30 * pulse)
        color_intensity = int(255 * pulse)
        cv2.circle(overlay, (150, 150), radius, (color_intensity, 100, 255), -1)
        
        # Moving rectangle
        t = time.time()
        x = int(400 + 100 * math.sin(t))
        y = 100
        self.detector.ui.draw_modern_rounded_rect(overlay, x, y, 80, 80, 15, (255, 255, 100))
        
        # Color transition demo
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        color_progress = (t % 4) / 4
        color_index = int(color_progress * len(colors))
        next_index = (color_index + 1) % len(colors)
        local_progress = (color_progress * len(colors)) % 1
        
        current_color = self.detector.ui.animation_manager.animate_color_transition(
            colors[color_index], colors[next_index], local_progress
        )
        
        cv2.rectangle(overlay, (400, 250), (500, 350), current_color, -1)
        
        # Add title
        cv2.putText(overlay, "✨ Animation System Demo", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return overlay
    
    def demo_emotion_history(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate emotion history visualization"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Simulate emotion history data
        history_length = 50
        emotions = list(COLOR_MAP.keys())
        
        # Generate fake history for demo
        fake_history = []
        for i in range(history_length):
            emotion = random.choice(emotions)
            confidence = 0.3 + 0.7 * random.random()
            fake_history.append({
                'timestamp': time.time() - (history_length - i),
                'emotion': emotion,
                'confidence': confidence
            })
        
        # Draw history graph
        graph_x, graph_y = 50, 100
        graph_w, graph_h = 500, 200
        
        # Background
        cv2.rectangle(overlay, (graph_x, graph_y), (graph_x + graph_w, graph_y + graph_h), 
                     (40, 40, 40), -1)
        
        # Plot points
        if len(fake_history) > 1:
            points = []
            for i, entry in enumerate(fake_history):
                px = graph_x + int((i / len(fake_history)) * graph_w)
                py = graph_y + graph_h - int(entry['confidence'] * graph_h)
                points.append((px, py))
                
                # Color based on emotion
                color = COLOR_MAP[entry['emotion']]['primary']
                cv2.circle(overlay, (px, py), 3, color, -1)
            
            # Draw connecting lines
            for i in range(1, len(points)):
                cv2.line(overlay, points[i-1], points[i], (100, 255, 255), 2)
        
        # Add legend
        legend_y = graph_y + graph_h + 50
        for i, (emotion, colors) in enumerate(COLOR_MAP.items()):
            legend_x = graph_x + (i % 4) * 130
            if i >= 4:
                legend_y += 30
            
            cv2.circle(overlay, (legend_x, legend_y), 8, colors['primary'], -1)
            cv2.putText(overlay, emotion.title(), (legend_x + 20, legend_y + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Add title
        cv2.putText(overlay, "📊 Emotion History Visualization", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return overlay
    
    def demo_face_detection(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate enhanced face detection"""
        # Use actual emotion detection but enhance the visualization
        processed_frame, emotion_data = self.detector.process_frame(frame)
        
        # Add demo title overlay
        cv2.putText(processed_frame, "🎭 Enhanced Face Detection", (50, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # Add feature callouts if faces detected
        if emotion_data["faces"]:
            callouts = [
                "• Animated borders",
                "• Confidence bars", 
                "• Modern styling",
                "• Real-time updates"
            ]
            
            for i, callout in enumerate(callouts):
                cv2.putText(processed_frame, callout, (50, 100 + i * 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)
        
        return processed_frame
    
    def demo_performance(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate performance improvements"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Performance metrics
        fps_history = getattr(self.detector, 'fps_history', [30] * 10)
        avg_fps = sum(fps_history) / len(fps_history) if fps_history else 30
        
        metrics = [
            f"FPS: {avg_fps:.1f}",
            f"Frame Skip: {getattr(self.detector, 'emotion_skip_frames', 3)}",
            f"History Size: {len(getattr(self.detector, 'emotion_history', []))}",
            f"TTS Threading: {'Enabled' if getattr(self.detector, 'tts_thread', None) else 'Disabled'}",
        ]
        
        # Draw performance panel
        panel_x, panel_y = 50, 100
        panel_w, panel_h = 400, 200
        
        self.detector.ui.draw_modern_rounded_rect(
            overlay, panel_x, panel_y, panel_w, panel_h, 20,
            color=(50, 50, 80), alpha=0.8
        )
        
        # Performance bars
        for i, metric in enumerate(metrics):
            y_pos = panel_y + 40 + i * 35
            cv2.putText(overlay, metric, (panel_x + 20, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Demo bar
            bar_x = panel_x + 250
            bar_w = 100
            bar_h = 15
            value = 0.7 + 0.3 * math.sin(time.time() + i)  # Demo animation
            
            self.detector.ui.draw_confidence_bar(
                overlay, bar_x, y_pos - 10, bar_w, bar_h, value, (100, 255, 100)
            )
        
        # Add title
        cv2.putText(overlay, "🔄 Performance Optimizations", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return overlay
    
    def demo_audio(self, frame: np.ndarray) -> np.ndarray:
        """Demonstrate audio features"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Audio waveform visualization
        wave_x, wave_y = 50, 150
        wave_w, wave_h = 500, 100
        
        # Background
        cv2.rectangle(overlay, (wave_x, wave_y), (wave_x + wave_w, wave_y + wave_h),
                     (30, 30, 30), -1)
        
        # Animated waveform
        t = time.time()
        points = []
        for i in range(0, wave_w, 5):
            x = wave_x + i
            wave_val = math.sin(t * 5 + i * 0.1) * 30
            y = wave_y + wave_h // 2 + int(wave_val)
            points.append((x, y))
        
        # Draw waveform
        for i in range(1, len(points)):
            cv2.line(overlay, points[i-1], points[i], (100, 255, 255), 2)
        
        # Audio features list
        features = [
            "🎵 Non-blocking TTS",
            "🔊 Voice Selection", 
            "⏱️ Smart Cooldowns",
            "🎭 Emotion-based Speech"
        ]
        
        for i, feature in enumerate(features):
            cv2.putText(overlay, feature, (50, 300 + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add title
        cv2.putText(overlay, "🎵 Enhanced Audio System", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return overlay
    
    def run_demo(self):
        """Run the interactive demo"""
        print("🎯 MoodLyft-Mirror Feature Demo")
        print("Controls:")
        print("  SPACE - Next demo")
        print("  R - Reset to first demo") 
        print("  Q - Quit demo")
        print("  S - Save screenshot")
        print("\nStarting demo...")
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                frame = cv2.flip(frame, 1)
                
                # Run current demo
                demo_name, demo_func = self.demo_features[self.current_demo]
                processed_frame = demo_func(frame)
                
                # Add demo navigation info
                nav_text = f"Demo {self.current_demo + 1}/{len(self.demo_features)}: {demo_name}"
                cv2.putText(processed_frame, nav_text, (10, processed_frame.shape[0] - 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                
                cv2.putText(processed_frame, "SPACE: Next | R: Reset | Q: Quit | S: Screenshot", 
                           (10, processed_frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                
                cv2.imshow("MoodLyft-Mirror Demo", processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):  # Space bar
                    self.current_demo = (self.current_demo + 1) % len(self.demo_features)
                    print(f"Switching to: {self.demo_features[self.current_demo][0]}")
                elif key == ord('r'):
                    self.current_demo = 0
                    print(f"Reset to: {self.demo_features[self.current_demo][0]}")
                elif key == ord('s'):
                    timestamp = int(time.time())
                    filename = f"demo_screenshot_{timestamp}.jpg"
                    cv2.imwrite(filename, processed_frame)
                    print(f"Screenshot saved: {filename}")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Demo ended. Thank you!")

def main():
    """Main demo function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
MoodLyft-Mirror Demo

This demo showcases all the features and optimizations:
• Modern glassmorphism UI effects
• Smooth animations and transitions  
• Real-time emotion history visualization
• Enhanced face detection with confidence bars
• Performance optimizations and metrics
• Improved audio system with threading

Usage:
  python demo.py              # Run interactive demo
  python demo.py --help       # Show this help
        """)
        return
    
    demo = FeatureDemo()
    demo.run_demo()

if __name__ == "__main__":
    main() 