#!/usr/bin/env python3
"""
TTS Manager Module
Handles text-to-speech functionality with thread safety and error handling
"""

import time
import logging
import random
import pyttsx3
import threading
import queue
from typing import Optional, List, Dict

from .config import (
    COMPLIMENTS, TTS_RATE, TTS_VOLUME, TTS_PREFERRED_VOICES,
    COMPLIMENT_COOLDOWN, NO_FACE_COOLDOWN
)

########################################
# TTS MANAGER
########################################
class TTSManager:
    """Thread-safe TTS manager with robust error handling"""
    
    def __init__(self):
        self.engine = None
        self.available = False
        self.current_voice = None
        self.speech_queue = queue.Queue(maxsize=5)
        self.worker_thread = None
        self.is_running = True
        
        logging.info("Initializing TTS engine...")
        
        if self._initialize_engine():
            self._start_worker()
            logging.info("✅ TTS engine initialized successfully")
        else:
            logging.warning("⚠️ TTS engine initialization failed - continuing without TTS")
    
    def _initialize_engine(self) -> bool:
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            if self.engine:
                self._configure_engine()
                self.available = True
                return True
        except Exception as e:
            logging.error(f"TTS initialization failed: {e}")
        
        self.available = False
        return False
    
    def _configure_engine(self):
        """Configure TTS engine properties"""
        try:
            self.engine.setProperty('rate', TTS_RATE)
            self.engine.setProperty('volume', TTS_VOLUME)
            logging.info("TTS engine configured successfully")
            
            # Set preferred voice
            self._set_preferred_voice()
            
        except Exception as e:
            logging.warning(f"TTS configuration warning: {e}")
    
    def _set_preferred_voice(self):
        """Set preferred voice if available"""
        try:
            voices = self.engine.getProperty('voices')
            if not voices:
                return
            
            # Try to find preferred voice
            for voice in voices:
                for preference in TTS_PREFERRED_VOICES:
                    if preference.lower() in voice.name.lower():
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
        
        # On macOS, prioritize system 'say' command for reliability
        import platform
        use_system_say = platform.system() == "Darwin"
        
        # Create a new engine instance for this thread only if not using system say
        thread_engine = None
        if not use_system_say:
            try:
                import pyttsx3
                thread_engine = pyttsx3.init()
                if thread_engine:
                    thread_engine.setProperty('rate', TTS_RATE)  # Use config value
                    thread_engine.setProperty('volume', TTS_VOLUME)
                    # Copy voice settings from main engine
                    if self.engine:
                        try:
                            main_voice = self.engine.getProperty('voice')
                            thread_engine.setProperty('voice', main_voice)
                        except:
                            pass
            except Exception as e:
                logging.warning(f"Could not create thread TTS engine: {e}")
                thread_engine = None
                use_system_say = True  # Fall back to system say
        
        while self.is_running:
            try:
                # Get speech request from queue with timeout
                text = self.speech_queue.get(timeout=1.0)
                
                if text and self.available:
                    try:
                        logging.info(f"🔊 Speaking: {text}")
                        if use_system_say:
                            # Use macOS system say command (most reliable)
                            import subprocess
                            result = subprocess.run(
                                ["say", "-r", str(TTS_RATE), text], 
                                capture_output=True, 
                                timeout=10
                            )
                            if result.returncode == 0:
                                logging.info("✅ TTS speech completed successfully (system say)")
                            else:
                                logging.warning(f"System say failed: {result.stderr}")
                        elif thread_engine:
                            thread_engine.say(text)
                            thread_engine.runAndWait()
                            logging.info("✅ TTS speech completed successfully (pyttsx3)")
                        else:
                            logging.warning("⚠️ No TTS method available")
                    except Exception as speech_error:
                        logging.error(f"❌ TTS speech error: {speech_error}")
                        # Don't stop the worker, just skip this speech
                
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"TTS worker error: {e}")
                # Continue without breaking - TTS is not critical
                continue
                
        # Clean up thread engine
        if thread_engine:
            try:
                thread_engine.stop()
            except:
                pass
                
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


########################################
# EMOTION FEEDBACK MANAGER
########################################
class EmotionFeedbackManager:
    """Manages emotion-based feedback with intelligent timing"""
    
    def __init__(self, tts_manager: TTSManager):
        self.tts = tts_manager
        self.last_compliment_time = 0
        self.last_no_face_message_time = 0
        self.consecutive_emotions = {}
        self.emotion_stability_threshold = 1  # Reduced from 2 to 1 second for easier testing
        self.last_emotion_change_time = time.time()
        
    def should_give_compliment(self, emotion: str, confidence: float) -> bool:
        """Determine if a compliment should be given"""
        current_time = time.time()
        
        # Check cooldown
        time_since_last = current_time - self.last_compliment_time
        if time_since_last < COMPLIMENT_COOLDOWN:
            logging.debug(f"Compliment blocked by cooldown: {time_since_last:.1f}s < {COMPLIMENT_COOLDOWN}s")
            return False
        
        # Check confidence threshold
        if confidence < 0.6:
            logging.debug(f"Compliment blocked by low confidence: {confidence:.2f} < 0.6")
            return False
        
        # Track emotion stability
        if emotion not in self.consecutive_emotions:
            self.consecutive_emotions[emotion] = current_time
            logging.debug(f"Starting emotion tracking for {emotion}")
            return False
        
        # Check if emotion has been stable long enough
        emotion_duration = current_time - self.consecutive_emotions[emotion]
        if emotion_duration >= self.emotion_stability_threshold:
            logging.info(f"✅ Compliment approved! Emotion {emotion} stable for {emotion_duration:.1f}s (confidence: {confidence:.2f})")
            return True
        else:
            logging.debug(f"Emotion {emotion} not stable enough: {emotion_duration:.1f}s < {self.emotion_stability_threshold}s")
        
        return False
    
    def give_compliment(self, emotion: str, confidence: float) -> Optional[str]:
        """Give appropriate compliment for the emotion"""
        try:
            if not self.should_give_compliment(emotion, confidence):
                return None
            
            compliments = COMPLIMENTS.get(emotion, COMPLIMENTS['neutral'])
            compliment = random.choice(compliments)
            
            # No emoji decorations - keep compliments clean for TTS
            
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