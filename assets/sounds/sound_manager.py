import os
import wave
import struct
import math
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from logging_config import logger
from storage.settings import SettingsManager

SOUNDS_DIR = os.path.join("assets", "sounds")

def generate_tone(filename, frequency, duration, volume=0.5, wave_type='sine'):
    """Generate a simple wave file programmatically."""
    if not os.path.exists(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR)
        
    filepath = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(filepath):
        return filepath # Use existing file
        
    try:
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(n_samples):
                t = float(i) / sample_rate
                
                if wave_type == 'sine':
                    value = math.sin(2.0 * math.pi * frequency * t)
                elif wave_type == 'square':
                    value = 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
                elif wave_type == 'sawtooth':
                    value = 2.0 * (t * frequency - math.floor(t * frequency + 0.5))
                else:
                    value = 0
                    
                # Envelope: simple fade in and out to prevent clicking
                fade_dur = 0.05
                if t < fade_dur:
                    value *= (t / fade_dur)
                elif t > duration - fade_dur:
                    value *= ((duration - t) / fade_dur)
                    
                sample = int(value * volume * 32767.0)
                wav_file.writeframes(struct.pack('h', sample))
                
        logger.info(f"Generated default sound: {filename}")
    except Exception as e:
        logger.error(f"Failed to generate sound {filename}: {e}")
        
    return filepath

class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.settings = SettingsManager()
            cls._instance.effects = {}
            cls._instance._init_sounds()
        return cls._instance
        
    def _init_sounds(self):
        # Define base sounds to generate if missing
        sound_defs = {
            "correct": {"freq": 880.0, "dur": 0.15, "type": "sine"},
            "wrong": {"freq": 150.0, "dur": 0.3, "type": "sawtooth"},
            "win": {"freq": 523.25, "dur": 1.0, "type": "sine"}, # C5
            "loss": {"freq": 130.81, "dur": 1.0, "type": "sawtooth"}, # C3
            "click": {"freq": 1000.0, "dur": 0.05, "type": "square"}
        }
        
        for name, params in sound_defs.items():
            filename = f"{name}.wav"
            filepath = os.path.join(SOUNDS_DIR, filename)
            
            # If the user provided a custom file, we don't overwrite it
            if not os.path.exists(filepath):
                generate_tone(filename, params["freq"], params["dur"], 0.3, params["type"])
                
            # Load into QSoundEffect
            if os.path.exists(filepath):
                effect = QSoundEffect()
                effect.setSource(QUrl.fromLocalFile(os.path.abspath(filepath)))
                self.effects[name] = effect
                
    def play(self, sound_name):
        if not self.settings.get("sound_enabled"):
            return
            
        effect = self.effects.get(sound_name)
        if effect:
            # Replay if already playing
            if effect.isPlaying():
                effect.stop()
            effect.play()
        else:
            logger.warning(f"Sound '{sound_name}' not found.")
