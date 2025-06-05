import time
import threading
import queue
import random
from typing import Dict, Optional, List
import logging

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not available. TTS features will be disabled.")

from .config import (
    COMPLIMENTS, TTS_RATE, TTS_VOLUME, TTS_PREFERRED_VOICES,
    COMPLIMENT_COOLDOWN, NO_FACE_COOLDOWN
)


class TTSManager:
    """Enhanced Text-to-Speech manager with threading and voice selection"""
    
    def __init__(self):
        self.engine = None
        self.available = False
        self.speech_queue = queue.Queue()
        self.worker_thread = None
        self.is_running = False
        self.current_voice = None
        self.initialization_attempted = False
        
        if TTS_AVAILABLE:
            self._initialize_engine()
            if self.available:
                self._start_worker()
    
    def _initialize_engine(self) -> bool:
        """Initialize the TTS engine with error handling"""
        if self.initialization_attempted:
            return self.available
            
        self.initialization_attempted = True
        try:
            logging.info("Initializing TTS engine...")
            self.engine = pyttsx3.init()
            self._configure_engine()
            self.available = True
            logging.info("✅ TTS engine initialized successfully")
            return True
        except Exception as e:
            logging.warning(f"⚠️ TTS engine initialization failed: {e}")
            logging.info("🔇 TTS will be disabled, but application will continue normally")
            self.available = False
            self.engine = None
            return False
    
    def _configure_engine(self):
        """Configure TTS engine settings"""
        if not self.engine:
            return
        
        try:
            # Set speech rate
            self.engine.setProperty('rate', TTS_RATE)
            
            # Set volume
            self.engine.setProperty('volume', TTS_VOLUME)
            
            # Try to set preferred voice
            self._set_preferred_voice()
            
            logging.info("TTS engine configured successfully")
            
        except Exception as e:
            logging.warning(f"Failed to configure TTS engine: {e}")
            # Don't disable TTS entirely for configuration errors
    
    def _set_preferred_voice(self):
        """Set preferred voice based on configuration"""
        if not self.engine:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if not voices:
                logging.warning("No TTS voices available")
                return
            
            # Try to find preferred voice
            for voice in voices:
                voice_id = voice.id.lower()
                voice_name = voice.name.lower() if voice.name else ""
                
                for preferred in TTS_PREFERRED_VOICES:
                    if preferred.lower() in voice_id or preferred.lower() in voice_name:
                        self.engine.setProperty('voice', voice.id)
                        self.current_voice = voice.name
                        logging.info(f"Set TTS voice to: {voice.name}")
                        return
            
            # Fallback to first available voice
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                self.current_voice = voices[0].name
                logging.info(f"Using default voice: {voices[0].name}")
                
        except Exception as e:
            logging.warning(f"Failed to set voice: {e}")
    
    def _start_worker(self):
        """Start the TTS worker thread"""
        if self.worker_thread and self.worker_thread.is_alive():
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()
        logging.info("TTS worker thread started")
    
    def _speech_worker(self):
        """Worker thread for processing speech queue"""
        logging.info("TTS worker thread running")
        while self.is_running:
            try:
                # Get speech request from queue with timeout
                text = self.speech_queue.get(timeout=1.0)
                
                if text and self.available and self.engine:
                    try:
                        logging.debug(f"TTS speaking: {text[:50]}...")
                        self.engine.say(text)
                        self.engine.runAndWait()
                        logging.debug("TTS speech completed")
                    except Exception as speech_error:
                        logging.error(f"TTS speech error: {speech_error}")
                        # Don't stop the worker, just skip this speech
                
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"TTS worker error: {e}")
                # Try to reinitialize engine on critical error
                try:
                    if not self._initialize_engine():
                        logging.warning("TTS reinitialization failed, disabling TTS")
                        self.available = False
                        break
                except Exception as reinit_error:
                    logging.error(f"TTS reinitialization error: {reinit_error}")
                    self.available = False
                    break
                
        logging.info("TTS worker thread stopped")
    
    def speak_async(self, text: str) -> bool:
        """Add text to speech queue for async processing"""
        if not text or not text.strip():
            return False
            
        if not self.available:
            logging.debug(f"TTS not available, skipping: {text[:50]}...")
            return False
        
        try:
            # Clear queue if it's getting too full
            if self.speech_queue.qsize() > 3:
                try:
                    with self.speech_queue.mutex:
                        self.speech_queue.queue.clear()
                    logging.debug("Cleared TTS queue due to backlog")
                except:
                    pass
            
            self.speech_queue.put(text, block=False)
            logging.debug(f"Queued TTS: {text[:50]}...")
            return True
            
        except queue.Full:
            logging.warning("TTS queue is full, dropping speech request")
            return False
        except Exception as e:
            logging.error(f"Failed to queue speech: {e}")
            return False
    
    def speak_immediate(self, text: str) -> bool:
        """Speak text immediately (blocking)"""
        if not self.available or not text.strip() or not self.engine:
            return False
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logging.error(f"Immediate speech failed: {e}")
            return False
    
    def clear_queue(self):
        """Clear all pending speech requests"""
        try:
            with self.speech_queue.mutex:
                self.speech_queue.queue.clear()
        except Exception as e:
            logging.warning(f"Failed to clear TTS queue: {e}")
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_info = {
                    'id': voice.id,
                    'name': voice.name if voice.name else 'Unknown',
                    'languages': getattr(voice, 'languages', []),
                    'gender': getattr(voice, 'gender', 'Unknown')
                }
                voice_list.append(voice_info)
            
            return voice_list
            
        except Exception as e:
            logging.error(f"Failed to get voices: {e}")
            return []
    
    def set_voice_by_id(self, voice_id: str) -> bool:
        """Set voice by ID"""
        if not self.engine:
            return False
        
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if voice.id == voice_id:
                    self.engine.setProperty('voice', voice_id)
                    self.current_voice = voice.name
                    logging.info(f"Voice changed to: {voice.name}")
                    return True
            return False
        except Exception as e:
            logging.error(f"Failed to set voice: {e}")
            return False
    
    def stop(self):
        """Stop the TTS manager"""
        logging.info("Stopping TTS manager...")
        self.is_running = False
        self.clear_queue()
        
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                logging.warning(f"Error stopping TTS engine: {e}")
        
        logging.info("TTS manager stopped")


class EmotionFeedbackManager:
    """Manages emotion-based feedback with intelligent timing"""
    
    def __init__(self, tts_manager: TTSManager):
        self.tts = tts_manager
        self.last_compliment_time = 0
        self.last_no_face_message_time = 0
        self.consecutive_emotions = {}
        self.emotion_stability_threshold = 2  # Reduced from 3 to 2 seconds for easier testing
        self.last_emotion_change_time = time.time()
        
    def should_give_compliment(self, emotion: str, confidence: float) -> bool:
        """Determine if a compliment should be given"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_compliment_time < COMPLIMENT_COOLDOWN:
            return False
        
        # Check confidence threshold
        if confidence < 0.7:
            return False
        
        # Track emotion stability
        if emotion not in self.consecutive_emotions:
            self.consecutive_emotions[emotion] = current_time
            return False
        
        # Check if emotion has been stable long enough
        emotion_duration = current_time - self.consecutive_emotions[emotion]
        if emotion_duration >= self.emotion_stability_threshold:
            return True
        
        return False
    
    def give_compliment(self, emotion: str, confidence: float) -> Optional[str]:
        """Give appropriate compliment for the emotion"""
        try:
            if not self.should_give_compliment(emotion, confidence):
                return None
            
            compliments = COMPLIMENTS.get(emotion, COMPLIMENTS['neutral'])
            compliment = random.choice(compliments)
            
            # Add confidence-based enthusiasm
            if confidence > 0.9:
                compliment = f"✨ {compliment} ✨"
            elif confidence > 0.8:
                compliment = f"🌟 {compliment}"
            
            # Update timing
            self.last_compliment_time = time.time()
            
            # Reset emotion tracking
            self.consecutive_emotions.clear()
            
            # Queue for speech (non-blocking)
            success = self.tts.speak_async(compliment)
            if success:
                logging.info(f"Compliment given: {compliment}")
            else:
                logging.debug(f"Compliment shown (TTS unavailable): {compliment}")
            
            return compliment
            
        except Exception as e:
            logging.error(f"Error giving compliment: {e}")
            return None
    
    def handle_no_face_detected(self) -> Optional[str]:
        """Handle when no face is detected"""
        try:
            current_time = time.time()
            
            if current_time - self.last_no_face_message_time < NO_FACE_COOLDOWN:
                return None
            
            messages = [
                "I'm here when you're ready! 👋",
                "Looking for your beautiful face! 😊",
                "Come back when you're ready to smile! ✨",
                "Waiting to see that wonderful expression! 🌟"
            ]
            
            message = random.choice(messages)
            self.last_no_face_message_time = current_time
            
            # Queue for speech (non-blocking)
            self.tts.speak_async(message)
            
            return message
            
        except Exception as e:
            logging.error(f"Error handling no face: {e}")
            return None
    
    def update_emotion_tracking(self, emotion: str, confidence: float):
        """Update emotion tracking for stability analysis"""
        try:
            current_time = time.time()
            
            # Clear tracking for low confidence emotions
            if confidence < 0.6:
                self.consecutive_emotions.clear()
                return
            
            # If emotion changed, reset tracking
            if emotion not in self.consecutive_emotions:
                self.consecutive_emotions.clear()
                self.consecutive_emotions[emotion] = current_time
                self.last_emotion_change_time = current_time
            
            # Clean up old emotions
            emotions_to_remove = []
            for tracked_emotion, start_time in self.consecutive_emotions.items():
                if tracked_emotion != emotion and current_time - start_time > 1.0:
                    emotions_to_remove.append(tracked_emotion)
            
            for old_emotion in emotions_to_remove:
                del self.consecutive_emotions[old_emotion]
                
        except Exception as e:
            logging.error(f"Error updating emotion tracking: {e}")
    
    def get_emotion_stability_info(self) -> Dict:
        """Get current emotion stability information"""
        try:
            current_time = time.time()
            stability_info = {}
            
            for emotion, start_time in self.consecutive_emotions.items():
                duration = current_time - start_time
                stability_info[emotion] = {
                    'duration': duration,
                    'stable': duration >= self.emotion_stability_threshold
                }
            
            return stability_info
            
        except Exception as e:
            logging.error(f"Error getting stability info: {e}")
            return {} 