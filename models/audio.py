import numpy as np
import librosa
import tensorflow as tf
from scipy import signal
from typing import Dict, List, Tuple
import json

class AudioProcessor:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.sound_classes = [
            "bird_call", "wind", "rain", "insect", "mammal", 
            "water_flow", "thunder", "rustling", "silence", "human_activity"
        ]
        
    def extract_features(self, audio_data: np.ndarray) -> Dict:
        """Extract comprehensive audio features"""
        # Ensure audio is float32
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32) / 32768.0
            
        features = {}
        
        # Basic features
        features['rms'] = float(np.sqrt(np.mean(audio_data**2)))
        features['zero_crossing_rate'] = float(np.mean(librosa.feature.zero_crossing_rate(audio_data)[0]))
        
        # Spectral features
        stft = librosa.stft(audio_data)
        magnitude = np.abs(stft)
        
        features['spectral_centroid'] = float(np.mean(librosa.feature.spectral_centroid(S=magnitude)[0]))
        features['spectral_rolloff'] = float(np.mean(librosa.feature.spectral_rolloff(S=magnitude)[0]))
        features['spectral_bandwidth'] = float(np.mean(librosa.feature.spectral_bandwidth(S=magnitude)[0]))
        
        # MFCCs
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
        for i in range(13):
            features[f'mfcc_{i}'] = float(np.mean(mfccs[i]))
            
        # Chroma features
        chroma = librosa.feature.chroma_stft(S=magnitude)
        features['chroma_mean'] = float(np.mean(chroma))
        
        # Tempo and rhythm
        tempo, _ = librosa.beat.beat_track(y=audio_data, sr=self.sample_rate)
        features['tempo'] = float(tempo)
        
        return features
    
    def detect_sound_events(self, audio_data: np.ndarray) -> List[Dict]:
        """Detect and classify sound events"""
        features = self.extract_features(audio_data)
        
        # Simple rule-based classification (replace with trained model)
        events = []
        
        if features['rms'] > 0.01:
            if features['spectral_centroid'] > 3000:
                if features['zero_crossing_rate'] > 0.1:
                    events.append({
                        "type": "bird_call",
                        "confidence": min(features['spectral_centroid'] / 5000, 1.0),
                        "frequency_range": [2000, 8000]
                    })
            elif features['spectral_centroid'] < 1000:
                if features['spectral_rolloff'] < 2000:
                    events.append({
                        "type": "wind",
                        "confidence": min(features['rms'] * 10, 1.0),
                        "frequency_range": [20, 1000]
                    })
            elif 1000 <= features['spectral_centroid'] <= 3000:
                events.append({
                    "type": "rustling",
                    "confidence": features['rms'] * 5,
                    "frequency_range": [500, 3000]
                })
        
        # Detect patterns for different animals/environmental sounds
        if features['tempo'] > 120 and features['spectral_bandwidth'] > 1000:
            events.append({
                "type": "insect",
                "confidence": 0.7,
                "frequency_range": [1000, 6000]
            })
            
        return events
    
    def analyze_environmental_stress(self, features: Dict) -> Dict:
        """Analyze audio for signs of environmental stress"""
        stress_indicators = {
            "noise_pollution": features['rms'] > 0.1,
            "unusual_frequency_pattern": features['spectral_centroid'] > 4000 or features['spectral_centroid'] < 200,
            "high_activity": features['zero_crossing_rate'] > 0.2,
            "silence_anomaly": features['rms'] < 0.001
        }
        
        stress_level = sum(stress_indicators.values()) / len(stress_indicators)
        
        return {
            "stress_level": stress_level,
            "indicators": stress_indicators,
            "interpretation": self._interpret_stress(stress_level, stress_indicators)
        }
    
    def _interpret_stress(self, level: float, indicators: Dict) -> str:
        """Interpret stress level into human-readable format"""
        if level > 0.7:
            return "High environmental stress detected"
        elif level > 0.4:
            return "Moderate environmental changes observed"
        elif level > 0.2:
            return "Minor environmental variations"
        else:
            return "Calm environmental conditions"
    
    def process_real_time(self, audio_chunk: np.ndarray) -> Dict:
        """Process real-time audio chunk"""
        features = self.extract_features(audio_chunk)
        events = self.detect_sound_events(audio_chunk)
        stress_analysis = self.analyze_environmental_stress(features)
        
        return {
            "features": features,
            "detected_events": events,
            "stress_analysis": stress_analysis,
            "timestamp": np.datetime64('now').astype(str)
        }