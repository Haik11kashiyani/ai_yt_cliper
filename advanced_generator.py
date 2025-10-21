import os
import cv2
import numpy as np
from moviepy.editor import *
import whisper
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import librosa
import soundfile as sf
from scipy.signal import find_peaks
import json

class AdvancedShortsGenerator:
    def __init__(self):
        # Load models
        try:
            self.whisper_model = whisper.load_model("base")
        except AttributeError:
            # Fallback for different whisper versions
            import whisper
            self.whisper_model = whisper.load_model("base")
        
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Sentiment analysis model
        self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                         model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        
        # Emotion detection
        self.emotion_analyzer = pipeline("text-classification", 
                                       model="j-hartmann/emotion-english-distilroberta-base")
        
    def analyze_audio_features(self, audio_path):
        """Audio features analyze करके emotional peaks find करता है"""
        print("🎵 Analyzing audio features...")
        
        # Load audio
        y, sr = librosa.load(audio_path)
        
        # Extract features
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        energy = librosa.feature.rms(y=y)[0]
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        
        # Find energy peaks (exciting moments)
        energy_peaks, _ = find_peaks(energy, height=np.mean(energy) + np.std(energy))
        
        # Convert frame indices to time
        frame_times = librosa.frames_to_time(np.arange(len(energy)), sr=sr)
        peak_times = frame_times[energy_peaks]
        
        return {
            "tempo": tempo,
            "energy_peaks": peak_times.tolist(),
            "avg_energy": np.mean(energy),
            "energy_variance": np.var(energy)
        }
    
    def detect_visual_interest(self, video_path, start_time, end_time):
        """Visual interest detect करता है - motion, faces, objects"""
        print("👁️ Analyzing visual interest...")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        
        # Motion detection
        motion_scores = []
        face_counts = []
        
        prev_frame = None
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        frame_count = 0
        while cap.isOpened() and frame_count < (end_frame - start_frame):
            ret, frame = cap.read()
            if not ret:
                break
            
            # Motion detection
            if prev_frame is not None:
                diff = cv2.absdiff(prev_frame, frame)
                motion_score = np.mean(diff)
                motion_scores.append(motion_score)
            
            # Face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            face_counts.append(len(faces))
            
            prev_frame = frame.copy()
            frame_count += 1
        
        cap.release()
        
        return {
            "avg_motion": np.mean(motion_scores) if motion_scores else 0,
            "max_motion": np.max(motion_scores) if motion_scores else 0,
            "avg_faces": np.mean(face_counts),
            "max_faces": np.max(face_counts),
            "motion_variance": np.var(motion_scores) if motion_scores else 0
        }
    
    def advanced_content_analysis(self, segments, audio_features):
        """Advanced content analysis with multiple factors"""
        print("🧠 Advanced content analysis...")
        
        viral_moments = []
        
        for i, segment in enumerate(segments):
            text = segment["text"]
            start_time = segment["start"]
            end_time = segment["end"]
            
            # Text analysis
            sentiment = self.sentiment_analyzer(text)[0]
            emotion = self.emotion_analyzer(text)[0]
            
            # Audio analysis for this segment
            segment_energy = self.get_segment_energy(audio_features, start_time, end_time)
            
            # Calculate viral score
            viral_score = self.calculate_viral_score(text, sentiment, emotion, segment_energy)
            
            viral_moments.append({
                "text": text,
                "start": start_time,
                "end": end_time,
                "sentiment": sentiment,
                "emotion": emotion,
                "energy": segment_energy,
                "viral_score": viral_score
            })
        
        # Sort by viral score
        viral_moments.sort(key=lambda x: x["viral_score"], reverse=True)
        
        return viral_moments[:10]
    
    def get_segment_energy(self, audio_features, start_time, end_time):
        """Segment के लिए energy calculate करता है"""
        peaks_in_segment = [p for p in audio_features["energy_peaks"] 
                           if start_time <= p <= end_time]
        return len(peaks_in_segment) / (end_time - start_time) if end_time > start_time else 0
    
    def calculate_viral_score(self, text, sentiment, emotion, energy):
        """Viral score calculate करता है multiple factors के basis पर"""
        score = 0
        
        # Sentiment score
        if sentiment["label"] == "POSITIVE":
            score += sentiment["score"] * 2
        elif sentiment["label"] == "NEGATIVE":
            score += sentiment["score"] * 1.5  # Negative can also be viral
        
        # Emotion score
        high_impact_emotions = ["joy", "surprise", "anger", "fear"]
        if emotion["label"] in high_impact_emotions:
            score += emotion["score"] * 1.5
        
        # Energy score
        score += energy * 10
        
        # Text length bonus (not too short, not too long)
        word_count = len(text.split())
        if 5 <= word_count <= 20:
            score += 0.5
        
        # Viral keywords bonus
        viral_keywords = [
            "amazing", "incredible", "unbelievable", "shocking", "wow", "omg",
            "अद्भुत", "अविश्वसनीय", "चौंकाने वाला", "वाह", "क्या बात है"
        ]
        
        keyword_count = sum(1 for keyword in viral_keywords if keyword.lower() in text.lower())
        score += keyword_count * 0.3
        
        return score
    
    def create_advanced_short(self, video_path, start_time, end_time, output_path, 
                            text_content, visual_data, audio_data):
        """Advanced short video creation with better effects"""
        print(f"🎬 Creating advanced short: {output_path}")
        
        # Extract video clip
        video = VideoFileClip(video_path)
        clip = video.subclip(start_time, end_time)
        
        # Resize to 9:16 aspect ratio
        clip = clip.resize(height=1920)
        clip = clip.resize(width=1080)
        
        # Apply visual effects based on analysis
        if visual_data["max_faces"] > 1:
            clip = self.create_advanced_side_by_side(clip, visual_data)
        else:
            clip = self.create_advanced_single_person(clip, visual_data)
        
        # Add dynamic background music
        clip = self.add_dynamic_music(clip, audio_data)
        
        # Add animated text overlay
        clip = self.add_animated_text(clip, text_content)
        
        # Add transitions
        clip = clip.fadein(0.3).fadeout(0.3)
        
        # Export
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac', 
                           verbose=False, logger=None)
        
        clip.close()
        video.close()
    
    def create_advanced_side_by_side(self, clip, visual_data):
        """Advanced side-by-side layout with effects"""
        width = clip.w
        height = clip.h
        
        # Create left and right clips with slight zoom
        left_clip = clip.crop(x1=0, x2=width//2, y1=0, y2=height)
        right_clip = clip.crop(x1=width//2, x2=width, y1=0, y2=height)
        
        # Add slight zoom effect
        left_clip = left_clip.resize(1.1).set_position(('left', 'center'))
        right_clip = right_clip.resize(1.1).set_position(('right', 'center'))
        
        # Create final composite
        final_clip = CompositeVideoClip([left_clip, right_clip], size=(1080, 1920))
        
        return final_clip
    
    def create_advanced_single_person(self, clip, visual_data):
        """Advanced single person layout with smart cropping"""
        # Smart crop based on motion
        if visual_data["motion_variance"] > 0.1:
            # High motion - keep more of the frame
            clip = clip.crop(width=1080, height=1920, x_center=clip.w/2, y_center=clip.h/2)
        else:
            # Low motion - tighter crop
            clip = clip.crop(width=1080, height=1920, x_center=clip.w/2, y_center=clip.h/2)
            clip = clip.resize(1.1)  # Slight zoom
        
        return clip
    
    def add_dynamic_music(self, clip, audio_data):
        """Dynamic background music based on audio analysis"""
        try:
            duration = clip.duration
            
            # Generate music based on tempo
            tempo = audio_data.get("tempo", 120)
            beat_duration = 60.0 / tempo
            
            # Create rhythmic audio
            t = np.linspace(0, duration, int(44100 * duration))
            audio_array = np.sin(2 * np.pi * 440 * t) * 0.02  # Low volume
            
            # Add beat pattern
            beat_times = np.arange(0, duration, beat_duration)
            for beat_time in beat_times:
                beat_start = int(beat_time * 44100)
                beat_end = int((beat_time + 0.1) * 44100)
                if beat_end < len(audio_array):
                    audio_array[beat_start:beat_end] *= 2
            
            # Create audio clip
            audio_clip = AudioClip(lambda t: audio_array[int(t * 44100)], duration=duration)
            audio_clip = audio_clip.volumex(0.05)  # 5% volume
            
            # Mix with original audio
            if clip.audio:
                final_audio = CompositeAudioClip([clip.audio, audio_clip])
                clip = clip.set_audio(final_audio)
            else:
                clip = clip.set_audio(audio_clip)
                
        except Exception as e:
            print(f"Dynamic music failed: {e}")
        
        return clip
    
    def add_animated_text(self, clip, text):
        """Animated text overlay with effects"""
        # Break text into lines
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 25:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Create animated text clips
        text_clips = []
        for i, line in enumerate(lines):
            # Text with animation
            txt_clip = TextClip(line, fontsize=45, color='white', font='Arial-Bold')
            txt_clip = txt_clip.set_position(('center', 150 + i * 50))
            
            # Add animation
            txt_clip = txt_clip.set_start(0.5).set_duration(clip.duration - 1)
            
            # Fade in/out
            txt_clip = txt_clip.fadein(0.3).fadeout(0.3)
            
            text_clips.append(txt_clip)
        
        # Background for text
        if text_clips:
            bg_clip = ColorClip(size=(1080, len(lines) * 50 + 20), 
                              color=(0, 0, 0), duration=clip.duration)
            bg_clip = bg_clip.set_position(('center', 130)).set_opacity(0.6)
            text_clips.insert(0, bg_clip)
        
        # Composite
        final_clip = CompositeVideoClip([clip] + text_clips)
        return final_clip
