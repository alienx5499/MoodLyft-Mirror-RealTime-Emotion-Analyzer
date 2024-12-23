import logging
import cv2
import numpy as np
from fer import FER
import pyttsx3
import random
import time
import math
import datetime
from typing import Tuple, Dict, List
import colorsys
from PIL import Image, ImageDraw, ImageFont
import platform
import os

########################################
# LOGGING CONFIGURATION
########################################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

########################################
# DIRECTORIES FOR OUTPUT
########################################
VIDEOS_DIR = "Output/Videos"
SCREENSHOTS_DIR = "Output/Screenshots"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

########################################
# ENHANCED EMOTION DATA
########################################
COMPLIMENTS = {
    "happy": [
        "Your smile brightens everyone's day!",
        "That genuine happiness is contagious!",
        "You have such a warm, inviting presence!",
        "Your joy creates ripples of positivity!",
        "Keep shining with that beautiful energy!"
    ],
    "neutral": [
        "Your calm presence is so grounding!",
        "There's strength in your composure!",
        "Your steady energy is admirable!",
        "You bring balance wherever you go!",
        "Your mindful presence is appreciated!"
    ],
    "sad": [
        "You're stronger than you know!",
        "Every storm passes - hang in there!",
        "Your resilience is truly inspiring!",
        "Better days are coming - believe it!",
        "You're never alone in this journey!"
    ],
    "angry": [
        "Channel that energy into positive change!",
        "Your passion can move mountains!",
        "Transform that fire into motivation!",
        "Your intensity can spark amazing things!",
        "Use that power to achieve greatness!"
    ],
    "surprise": [
        "Your wonderment is refreshing!",
        "Stay curious and keep exploring!",
        "Life is full of amazing discoveries!",
        "Your enthusiasm is infectious!",
        "Keep embracing new experiences!"
    ],
    "fear": [
        "Courage isn't fearlessness - it's facing fear!",
        "You're braver than you believe!",
        "Every step forward conquers fear!",
        "Your strength shines through uncertainty!",
        "Fear is temporary - your courage is permanent!"
    ],
    "disgust": [
        "Your standards show self-respect!",
        "Trust your instincts - they serve you well!",
        "Your boundaries protect your peace!",
        "Standing firm shows inner strength!",
        "Your authenticity is powerful!"
    ]
}

########################################
# ENHANCED COLOR SCHEME
########################################
COLOR_MAP = {
    "happy":   (255, 223, 0),    # Bright gold
    "neutral": (200, 200, 200),  # Subtle gray
    "sad":     (147, 112, 219),  # Purple
    "angry":   (220, 20, 60),    # Crimson
    "surprise":(255, 165, 0),    # Orange
    "fear":    (138, 43, 226),   # Blue violet
    "disgust": (50, 205, 50)     # Lime green
}

# Refined emoji set
EMOJIS = {
    "happy": "😊",
    "neutral": "😌",
    "sad": "🥺",
    "angry": "😤",
    "surprise": "😲",
    "fear": "😨",
    "disgust": "😖"
}

########################################
# UI UTILS
########################################
class UIElements:
    @staticmethod
    def create_gradient_background(width: int, height: int, 
                                   start_color: Tuple[int, int, int], 
                                   end_color: Tuple[int, int, int]) -> np.ndarray:
        """Creates a smooth gradient background top-to-bottom."""
        background = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            alpha = y / height
            color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * alpha)
                          for i in range(3))
            background[y, :] = color
        return background

    @staticmethod
    def create_rounded_rectangle(img: np.ndarray, x: int, y: int, 
                                 w: int, h: int, radius: int, 
                                 color: Tuple[int, int, int], thickness: int) -> None:
        """Draws a rounded rectangle on the image."""
        # Horizontal rectangles
        cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, thickness)
        cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, thickness)
        # Corner circles
        cv2.circle(img, (x + radius, y + radius), radius, color, thickness)
        cv2.circle(img, (x + w - radius, y + radius), radius, color, thickness)
        cv2.circle(img, (x + radius, y + h - radius), radius, color, thickness)
        cv2.circle(img, (x + w - radius, y + h - radius), radius, color, thickness)

    @staticmethod
    def add_glow_effect(img: np.ndarray, x: int, y: int, w: int, h: int, 
                        color: Tuple[int, int, int], intensity: int = 3) -> None:
        """Adds a subtle glow effect around a region."""
        for i in range(intensity):
            expanded = i * 2
            cv2.rectangle(
                img,
                (x - expanded, y - expanded),
                (x + w + expanded, y + h + expanded),
                color, 1
            )

########################################
# EMOTION DETECTOR
########################################
class EmotionDetector:
    def __init__(self):
        self.detector = FER(mtcnn=True)

        # Text-to-speech
        self.engine = pyttsx3.init()
        self.setup_voice()

        self.ui = UIElements()

        # TTS cooldown
        self.last_compliment_time = 0
        self.compliment_cooldown = 5

        # No-face cooldown
        self.last_no_face_time = 0
        self.no_face_cooldown = 5

        # Keep track of FPS
        self.prev_time = time.time()

        # Keep track of the last spoken compliment so we can keep displaying it
        self.last_spoken_compliment = ""

        # Load fonts
        self.fonts = self.load_fonts()

    def load_fonts(self):
        """Load fonts based on the operating system."""
        fonts = {}
        system = platform.system()
        try:
            if system == "Windows":
                fonts['default'] = ImageFont.truetype("arial.ttf", 20)
                fonts['fancy'] = ImageFont.truetype("arialbd.ttf", 30)
            elif system == "Darwin":  # macOS
                fonts['default'] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
                fonts['fancy'] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
            else:  # Linux and others
                fonts['default'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                fonts['fancy'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
            logging.info("Fonts loaded successfully.")
        except IOError:
            logging.error("Font file not found. Using default PIL font.")
            fonts['default'] = ImageFont.load_default()
            fonts['fancy'] = ImageFont.load_default()
        return fonts

    def setup_voice(self):
        """Configure TTS settings."""
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 0.8)
        for voice in self.engine.getProperty("voices"):
            if "en_US" in voice.id:
                self.engine.setProperty("voice", voice.id)
                break

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Process a single frame:
          - Add a gradient background
          - Detect emotions & draw bounding boxes with glow
          - Possibly speak compliments
          - Return final annotated frame + emotion data
        """
        # Copy for overlay
        overlay = frame.copy()
        h, w = frame.shape[:2]

        # 1) Add gradient background
        background = self.ui.create_gradient_background(w, h, (20, 20, 50), (50, 20, 70))
        cv2.addWeighted(overlay, 0.8, background, 0.2, 0, overlay)

        # 2) Detect emotions
        faces_data = self.detector.detect_emotions(frame)
        emotion_data = {"faces": faces_data, "dominant_emotion": None}

        if faces_data:
            # For each face
            for face_data in faces_data:
                self._process_face(overlay, face_data)

            # Single top emotion for compliments
            top_emotion = self.detector.top_emotion(frame)
            if top_emotion:
                emotion_data["dominant_emotion"] = top_emotion
                self._handle_emotion_feedback(top_emotion)
        else:
            # No face => TTS "No face detected" with cooldown
            now_nf = time.time()
            if (now_nf - self.last_no_face_time) > self.no_face_cooldown:
                logging.info("No face detected; speaking TTS message.")
                self.engine.say("No face detected.")
                self.engine.runAndWait()
                self.last_no_face_time = now_nf

        # 3) Additional UI elements (top banner, FPS, etc.)
        annotated_frame = self._add_ui_elements(overlay, frame)

        # 4) Return final annotated frame + emotion data
        return annotated_frame, emotion_data

    def _process_face(self, overlay: np.ndarray, face_data: Dict) -> None:
        """Draw bounding box + label for a single face."""
        x, y, w_box, h_box = face_data["box"]
        emotions = face_data["emotions"]
        best_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        color = COLOR_MAP.get(best_emotion, (200, 200, 200))

        # Glow effect bounding box
        self.ui.add_glow_effect(overlay, x, y, w_box, h_box, color)

        # Confidence
        confidence = emotions[best_emotion]
        label = f"{best_emotion.title()} ({confidence:.1%})"
        self._draw_emotion_label(overlay, label, x, y, w_box, color)

    def _handle_emotion_feedback(self, top_emotion_data: Tuple[str, float]) -> None:
        """Speak compliment if cooldown is over, store it for display."""
        emotion, confidence = top_emotion_data
        now = time.time()
        if (now - self.last_compliment_time) > self.compliment_cooldown:
            compliment = random.choice(COMPLIMENTS.get(emotion.lower(), COMPLIMENTS["neutral"]))
            # Speak compliment
            logging.info(f"Emotion: {emotion}, Confidence: {confidence:.2f}, Compliment: {compliment}")
            self.engine.say(compliment)
            self.engine.runAndWait()

            # Store it for display until next compliment
            self.last_spoken_compliment = f"{EMOJIS.get(emotion.lower(), '')} {compliment}"

            self.last_compliment_time = now
        else:
            # Do nothing extra, just keep showing last compliment if any
            pass

    def _add_ui_elements(self, overlay: np.ndarray, original_frame: np.ndarray) -> np.ndarray:
        """
        Add top banner, FPS counter, last compliment text, etc.
        Return final blended frame.
        """
        h, w = original_frame.shape[:2]

        # 1) Rounded rectangle for top banner
        self.ui.create_rounded_rectangle(overlay, 0, 0, w, 80, 10, (30, 30, 50), -1)

        # 2) FPS
        current_time = time.time()
        dt = current_time - self.prev_time
        fps = 1.0 / dt if dt > 0 else 0
        self.prev_time = current_time
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(overlay, fps_text, (20, 50), cv2.FONT_HERSHEY_DUPLEX, 0.7, (220, 220, 220), 1)

        # 3) If we have a last spoken compliment, display it near bottom center
        if self.last_spoken_compliment:
            # Convert overlay to PIL for better text handling
            pil_img = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_img)

            # Select font
            font = self.fonts.get('fancy', ImageFont.load_default())

            # Calculate text size
            text_bbox = draw.textbbox((0, 0), self.last_spoken_compliment, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate position
            x = (w - text_width) // 2
            y = h - 60  # Position 60 pixels from the bottom

            # Draw background rectangle with padding
            pad = 10
            background_rect = [
                x - pad,
                y - pad,
                x + text_width + pad,
                y + text_height + pad
            ]
            draw.rounded_rectangle(background_rect, radius=15, fill=(30, 30, 50, 180))

            # Draw text
            draw.text((x, y), self.last_spoken_compliment, font=font, fill=(255, 255, 255, 255))

            # Convert back to OpenCV image
            overlay = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # 4) Blend overlay
        final_frame = cv2.addWeighted(overlay, 0.7, original_frame, 0.3, 0)
        return final_frame

    def _draw_emotion_label(self, overlay: np.ndarray, text: str, x: int, y: int, 
                            w_box: int, color: Tuple[int, int, int]) -> None:
        """
        Draw emotion label just above the bounding box.
        """
        # Convert the OpenCV image to a PIL image
        pil_img = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        # Select font
        font = self.fonts.get('default', ImageFont.load_default())

        # Calculate text size using getbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Center the text above the bounding box
        text_x = x + (w_box - text_width) // 2
        text_y = y - text_height - 10

        # Draw background rectangle with padding
        pad = 5
        background_rect = [
            text_x - pad, 
            text_y - pad, 
            text_x + text_width + pad, 
            text_y + text_height + pad
        ]
        draw.rounded_rectangle(background_rect, radius=10, fill=color)

        # Draw text
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

        # Convert the PIL image back to OpenCV format
        overlay[:] = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

##############################################
#                 MAIN APP
##############################################
def main():
    logging.info("Starting 'MoodLyft-Mirror'.")
    logging.info("Press 'q' to quit, 's' to save a screenshot.")

    detector = EmotionDetector()
    cap = cv2.VideoCapture(0)

    # Configure camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Setup video writer (no audio)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(VIDEOS_DIR, f"emotion_capture_{timestamp}.mp4")
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (1280, 720))
    logging.info(f"Video will be saved at: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to grab frame from webcam.")
            time.sleep(0.1)
            continue

        frame = cv2.flip(frame, 1)  # Mirror effect
        processed_frame, _ = detector.process_frame(frame)

        # Write to video file
        out.write(processed_frame)

        # Display
        cv2.imshow("MoodLyft-Mirror", processed_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            logging.info("Exiting application via 'q' key.")
            break
        elif key == ord('s'):
            screenshot_name = f"emotion_screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
            cv2.imwrite(screenshot_path, frame)
            logging.info(f"Screenshot saved at: {screenshot_path}")

    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.info("Application closed successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        logging.info("Application crashed. Please check your setup and try again.")