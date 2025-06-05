import cv2
import numpy as np
import random
import time
from typing import Dict, List, Tuple

class SimpleFER:
    """Simple emotion detector for demonstration without FER dependency"""
    
    def __init__(self, mtcnn=False):
        # Ignore mtcnn parameter for compatibility
        self.emotions = ["happy", "sad", "angry", "surprise", "fear", "disgust", "neutral"]
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.last_emotion_time = {}
        self.emotion_stability = {}
        
    def detect_emotions(self, frame: np.ndarray) -> List[Dict]:
        """Detect faces and assign random emotions for demo - optimized for speed"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (320, 240))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
        
        # Scale back to original frame size
        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 240
        
        results = []
        for (x, y, w, h) in faces:
            # Scale back coordinates
            x = int(x * scale_x)
            y = int(y * scale_y)
            w = int(w * scale_x)
            h = int(h * scale_y)
            
            # Create stable emotion for each face position
            face_id = f"{x//50}_{y//50}"  # Rough face position ID
            
            current_time = time.time()
            
            # Change emotion every 3-5 seconds for demo
            if (face_id not in self.last_emotion_time or 
                current_time - self.last_emotion_time[face_id] > random.uniform(3, 5)):
                
                # Weighted random selection (more happy/neutral for demo)
                weights = [0.3, 0.1, 0.1, 0.15, 0.05, 0.05, 0.25]  # favor happy and neutral
                emotion = np.random.choice(self.emotions, p=weights)
                confidence = random.uniform(0.6, 0.95)
                
                self.emotion_stability[face_id] = (emotion, confidence)
                self.last_emotion_time[face_id] = current_time
            else:
                emotion, confidence = self.emotion_stability.get(face_id, ("neutral", 0.8))
            
            result = {
                'box': [x, y, w, h],
                'emotions': {emotion: confidence}
            }
            results.append(result)
            
        return results
    
    def top_emotion(self, frame: np.ndarray) -> Dict:
        """Get the top emotion for compatibility with FER API"""
        results = self.detect_emotions(frame)
        if results:
            # Get the first face's emotion
            first_face = results[0]
            emotions = first_face['emotions']
            top_emotion = max(emotions.items(), key=lambda x: x[1])
            return {top_emotion[0]: top_emotion[1]}
        return {}


class EmotionAnalyzer:
    """Wrapper class for emotion detection with additional functionality"""
    
    def __init__(self, use_mtcnn: bool = True):
        self.detector = SimpleFER(mtcnn=use_mtcnn)
        
    def analyze_frame(self, frame: np.ndarray) -> Tuple[List[Dict], Dict]:
        """
        Analyze frame for emotions and return results
        
        Returns:
            Tuple of (faces_data, dominant_emotion)
        """
        faces_data = self.detector.detect_emotions(frame)
        top_emotion = self.detector.top_emotion(frame)
        
        return faces_data, top_emotion
    
    def get_emotion_confidence(self, emotions_dict: Dict) -> float:
        """Get confidence score from emotions dictionary"""
        if not emotions_dict:
            return 0.0
        return max(emotions_dict.values())
    
    def get_dominant_emotion(self, emotions_dict: Dict) -> str:
        """Get the emotion with highest confidence"""
        if not emotions_dict:
            return "neutral"
        return max(emotions_dict.items(), key=lambda x: x[1])[0]
    
    def is_high_confidence(self, emotions_dict: Dict, threshold: float = 0.7) -> bool:
        """Check if the dominant emotion has high confidence"""
        confidence = self.get_emotion_confidence(emotions_dict)
        return confidence >= threshold 