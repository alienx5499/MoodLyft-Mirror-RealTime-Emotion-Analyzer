import logging
import cv2
import numpy as np
import time
import threading
import datetime
import os
from collections import deque
from typing import Tuple, Dict, Optional

# Import from our modular src package
from src.emotion_detector import EmotionAnalyzer
from src.animation import AnimationManager
from src.ui_elements import ModernUIElements
from src.tts_manager import TTSManager, EmotionFeedbackManager
from src.utils import load_fonts, get_system_info, get_border_style_for_emotion
from src.config import (
    COLOR_MAP, EMOJIS, EMOTION_SKIP_FRAMES,
    DEFAULT_CAMERA_WIDTH, DEFAULT_CAMERA_HEIGHT, DEFAULT_FPS,
    UI_PANEL_HEIGHT, UI_PANEL_PADDING, UI_ROUNDED_CORNER_RADIUS,
    VIDEOS_DIR, SCREENSHOTS_DIR
)

########################################
# LOGGING CONFIGURATION
########################################
logging.basicConfig(
    level=logging.INFO,  # Changed back to INFO to reduce noise, TTS messages will still show
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

########################################
# MAIN APPLICATION CLASS
########################################
class MoodLyftMirror:
    """Main application class that orchestrates all components"""
    
    def __init__(self):
        # Initialize components
        self.emotion_analyzer = EmotionAnalyzer(use_mtcnn=True)
        self.animation_manager = AnimationManager()
        self.ui_elements = ModernUIElements()
        self.tts_manager = TTSManager()
        self.feedback_manager = EmotionFeedbackManager(self.tts_manager)
        
        # Load fonts
        self.fonts = load_fonts()
        
        # Performance tracking
        self.frame_skip_count = 0
        self.last_emotion_result = None
        self.prev_time = time.time()
        self.fps_history = deque(maxlen=30)
        
        # State tracking
        self.emotion_history = deque(maxlen=30)
        self.current_emotion_color = (200, 200, 200)
        self.target_emotion_color = (200, 200, 200)
        self.color_transition_progress = 0
        self.last_compliment = ""
        
        logging.info("MoodLyft Mirror initialized successfully")
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """Process a single frame and return the enhanced result"""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Emotion detection with frame skipping for performance
        emotion_data = {"faces": [], "dominant_emotion": None}
        
        if self.frame_skip_count % EMOTION_SKIP_FRAMES == 0:
            try:
                faces_data, top_emotion = self.emotion_analyzer.analyze_frame(frame)
                self.last_emotion_result = (faces_data, top_emotion)
            except Exception as e:
                logging.error(f"Emotion detection error: {e}")
                faces_data, top_emotion = [], {}
        else:
            faces_data, top_emotion = self.last_emotion_result or ([], {})
        
        self.frame_skip_count += 1
        
        if faces_data:
            emotion_data["faces"] = faces_data
            
            # Process each face with enhanced visualization
            for face_data in faces_data:
                self._process_face(overlay, face_data)
            
            # Handle dominant emotion
            if top_emotion:
                emotion_data["dominant_emotion"] = top_emotion
                self._handle_emotion_feedback(top_emotion)
                
                # Update emotion history
                if isinstance(top_emotion, dict) and top_emotion:
                    emotion, confidence = list(top_emotion.items())[0]
                    self.emotion_history.append({
                        'timestamp': time.time(),
                        'emotion': emotion,
                        'confidence': confidence
                    })
        else:
            self._handle_no_face_detected()
        
        # Add UI elements
        final_frame = self._add_ui_elements(overlay, frame)
        
        return final_frame, emotion_data
    
    def _process_face(self, overlay: np.ndarray, face_data: Dict) -> None:
        """Process a single detected face"""
        x, y, w_box, h_box = face_data["box"]
        emotions = face_data["emotions"]
        best_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        confidence = emotions[best_emotion]
        
        # Get color scheme for emotion
        color_scheme = COLOR_MAP.get(best_emotion, COLOR_MAP['neutral'])
        primary_color = color_scheme['primary']
        
        # Smooth color transition
        if self.target_emotion_color != primary_color:
            self.target_emotion_color = primary_color
            self.color_transition_progress = 0
        
        if self.color_transition_progress < 1.0:
            self.color_transition_progress += 0.05
            self.current_emotion_color = self.ui_elements.animation_manager.animate_color_transition(
                self.current_emotion_color, self.target_emotion_color, self.color_transition_progress
            )
        
        # Draw enhanced face detection box
        self.ui_elements.draw_modern_rounded_rect(
            overlay, x - 10, y - 10, w_box + 20, h_box + 20, 15,
            color=self.current_emotion_color, alpha=0.3
        )
        
        # Enhanced animated border
        border_style = get_border_style_for_emotion(best_emotion)
        self.ui_elements.create_animated_border(overlay, x, y, w_box, h_box, 
                                     self.current_emotion_color, 4, border_style)
        
        # Enhanced emotion label
        self.ui_elements.draw_enhanced_emotion_label(
            overlay, best_emotion, confidence, x, y, w_box, color_scheme, self.fonts
        )
        
        # Confidence bar
        self.ui_elements.draw_confidence_bar(
            overlay, x, y + h_box + 10, w_box, 8, confidence, self.current_emotion_color
        )
    
    def _handle_emotion_feedback(self, top_emotion_data: Dict) -> None:
        """Handle emotion feedback through TTS"""
        try:
            logging.debug(f"Handling emotion feedback: {top_emotion_data}")
            if isinstance(top_emotion_data, dict) and top_emotion_data:
                emotion, confidence = list(top_emotion_data.items())[0]
                logging.debug(f"Processing emotion: {emotion} with confidence: {confidence}")
                
                # Update emotion tracking and give compliment if appropriate
                self.feedback_manager.update_emotion_tracking(emotion, confidence)
                compliment = self.feedback_manager.give_compliment(emotion, confidence)
                if compliment:
                    self.last_compliment = compliment
                    logging.debug(f"Compliment set: {compliment}")
                
                logging.debug("Emotion feedback handling completed")
        except Exception as e:
            logging.error(f"Error in emotion feedback: {e}", exc_info=True)
    
    def _handle_no_face_detected(self) -> None:
        """Handle no face detection"""
        try:
            message = self.feedback_manager.handle_no_face_detected()
            if message:
                self.last_compliment = message
        except Exception as e:
            logging.error(f"Error in no face handling: {e}")
    
    def _add_ui_elements(self, overlay: np.ndarray, original_frame: np.ndarray) -> np.ndarray:
        """Add all UI elements to the frame"""
        h, w = overlay.shape[:2]
        
        # Calculate FPS
        current_time = time.time()
        dt = current_time - self.prev_time
        fps = 1.0 / dt if dt > 0 else 0
        self.fps_history.append(fps)
        avg_fps = sum(self.fps_history) / len(self.fps_history)
        self.prev_time = current_time
        
        # Floating top panel
        panel_y = self.ui_elements.animation_manager.create_floating_animation(10, 3, 5.0)
        breath = self.ui_elements.animation_manager.create_breath_animation(6.0)
        panel_alpha = 0.6 + 0.1 * breath
        
        self.ui_elements.draw_modern_rounded_rect(
            overlay, 10, panel_y, w - 20, UI_PANEL_HEIGHT, 20,
            color=(20, 25, 35), alpha=panel_alpha
        )
        
        # App title
        self.ui_elements.draw_app_title(overlay, 30, panel_y + 35)
        
        # Performance indicators
        self.ui_elements.draw_fps_indicator(overlay, avg_fps, w - 150, 40)
        
        # Emotion history graph
        if len(self.emotion_history) > 1:
            self.ui_elements.draw_emotion_history_graph(overlay, w - 200, 50, 180, 30, self.emotion_history)
        
        # Enhanced compliment display
        if self.last_compliment:
            self.ui_elements.draw_enhanced_compliment(overlay, w, h, self.last_compliment, self.fonts)
        
        # Final blend
        return cv2.addWeighted(overlay, 0.9, original_frame, 0.1, 0)
    
    def setup_camera(self) -> cv2.VideoCapture:
        """Setup and configure camera"""
        logging.info("Setting up camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            logging.error("❌ Failed to open camera! Please check:")
            logging.error("   1. Camera is connected and not in use by another app")
            logging.error("   2. Camera permissions are granted")
            logging.error("   3. Try running: sudo killall VDCAssistant")
            raise RuntimeError("Camera initialization failed")
        
        # Configure camera for optimal performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, DEFAULT_CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DEFAULT_CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, DEFAULT_FPS)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
        
        logging.info("✅ Camera setup successful")
        return cap
    
    def setup_video_recording(self) -> cv2.VideoWriter:
        """Setup video recording if possible"""
        try:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = os.path.join(VIDEOS_DIR, f"emotion_capture_{timestamp}.mp4")
            return cv2.VideoWriter(video_path, fourcc, 30.0, (DEFAULT_CAMERA_WIDTH, DEFAULT_CAMERA_HEIGHT))
        except Exception as e:
            logging.warning(f"Video recording disabled: {e}")
            return None
    
    def handle_keyboard_input(self, key: int, processed_frame: np.ndarray) -> bool:
        """Handle keyboard input and return True if should continue"""
        if key == ord('q'):
            logging.info("Exiting application...")
            return False
        elif key == ord('s'):
            self._take_screenshot(processed_frame)
        elif key == ord('r'):
            self._reset_history()
        return True
    
    def _take_screenshot(self, frame: np.ndarray):
        """Take a screenshot"""
        try:
            screenshot_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
            cv2.imwrite(screenshot_path, frame)
            logging.info(f"Screenshot saved: {screenshot_path}")
            self.tts_manager.speak_async("Screenshot saved!")
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
    
    def _reset_history(self):
        """Reset emotion history"""
        try:
            self.emotion_history.clear()
            self.last_compliment = ""
            logging.info("Emotion history reset")
            self.tts_manager.speak_async("History cleared!")
        except Exception as e:
            logging.error(f"Error resetting history: {e}")
    
    def cleanup(self, cap: cv2.VideoCapture, out: cv2.VideoWriter):
        """Cleanup resources"""
        try:
            cap.release()
        except:
            pass
        try:
            if out is not None:
                out.release()
        except:
            pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        try:
            self.tts_manager.stop()
        except:
            pass

########################################
# MAIN FUNCTION
########################################
def main():
    """Main application entry point"""
    logging.info("Starting MoodLyft Mirror with modular architecture")
    logging.info("Controls: 'q' to quit, 's' for screenshot, 'r' to reset history")
    
    # Initialize application
    logging.info("Initializing MoodLyft Mirror application...")
    app = MoodLyftMirror()
    logging.info("✅ Application initialized successfully")
    
    # Setup camera and video recording
    logging.info("Setting up camera and video recording...")
    cap = app.setup_camera()
    out = app.setup_video_recording()
    logging.info("✅ Camera and video setup complete")
    
    logging.info("Starting main processing loop...")
    
    # Enable GUI mode for visual feedback AND audio
    headless_mode = False  # Changed from True to False to show the window
    if headless_mode:
        logging.info("🎯 Running in headless mode - audio-only emotion feedback")
        logging.info("💬 Listen for voice compliments based on your emotions!")
        logging.info("🔊 Make sure your speakers/headphones are on")
    else:
        logging.info("🎯 Running with GUI - visual AND audio emotion feedback")
        logging.info("👁️ You'll see your camera feed with emotion detection")
        logging.info("💬 Listen for voice compliments AND see visual feedback!")
        logging.info("🔊 Make sure your speakers/headphones are on")
        logging.info("⌨️ Press 'q' to quit, 's' for screenshot, 'r' to reset")
    
    try:
        frame_count = 0
        logging.info("Entering main while loop...")
        while True:
            try:
                frame_count += 1
                if frame_count % 100 == 0:  # Log every 100 frames instead of 30 for less noise
                    logging.info(f"Processing frame {frame_count}")
                
                ret, frame = cap.read()
                if not ret:
                    logging.warning("Failed to grab frame. Retrying...")
                    time.sleep(0.1)
                    continue
                
                # Mirror effect for natural interaction
                frame = cv2.flip(frame, 1)
                
                # Process frame
                processed_frame, emotion_data = app.process_frame(frame)
                
                # Record video if available
                if out is not None:
                    try:
                        out.write(processed_frame)
                    except Exception as e:
                        logging.warning(f"Video recording error: {e}")
                        out = None
                
                if headless_mode:
                    # Headless mode - just add a small delay for proper frame rate
                    time.sleep(0.033)  # ~30 FPS equivalent delay
                else:
                    # GUI mode - show the window
                    cv2.imshow("MoodLyft Mirror - Emotion Analyzer", processed_frame)
                    
                    # Handle keyboard input
                    key = cv2.waitKey(1) & 0xFF
                    if key != 255:  # A key was pressed
                        if not app.handle_keyboard_input(key, processed_frame):
                            break  # User pressed 'q' to quit
                    
            except Exception as frame_error:
                logging.error(f"Frame processing error: {frame_error}", exc_info=True)
                continue
    
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
    except Exception as e:
        logging.error(f"Application error: {e}", exc_info=True)
    finally:
        app.cleanup(cap, out)
        logging.info("Application closed successfully.")

if __name__ == "__main__":
    main() 