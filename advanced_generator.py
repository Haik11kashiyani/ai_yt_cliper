import os
import cv2
import numpy as np
from moviepy.editor import *
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper not available, using fallback mode")
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import librosa
import soundfile as sf
from scipy.signal import find_peaks
import json
from speaker_analyzer import SpeakerAnalyzer

class AdvancedShortsGenerator:
    def __init__(self):
        # Load models
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model("base")
            except Exception as e:
                print(f"⚠️ Whisper model loading failed: {e}")
                print("🔄 Using fallback mode...")
                self.whisper_model = None
        else:
            self.whisper_model = None
        
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Sentiment analysis model
        self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                         model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        
        # Emotion detection
        self.emotion_analyzer = pipeline("text-classification", 
                                       model="j-hartmann/emotion-english-distilroberta-base")
        
        # Speaker analyzer for conversation analysis
        self.speaker_analyzer = SpeakerAnalyzer()
        
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
        """Advanced content analysis with speaker diarization and meaningful moment detection"""
        print("🧠 Advanced AI content analysis with speaker detection...")
        
        # Analyze speakers and enhance segments
        enhanced_segments = self.speaker_analyzer.analyze_speakers("temp_audio.wav", segments)
        
        # Identify meaningful moments
        meaningful_moments = self.speaker_analyzer.identify_meaningful_moments(enhanced_segments)
        
        # Group into conversation threads
        conversation_threads = self.speaker_analyzer.group_conversation_threads(meaningful_moments)
        
        # Add audio analysis to threads
        for thread in conversation_threads:
            start_time = thread["start"]
            end_time = thread["end"]
            segment_energy = self.get_segment_energy(audio_features, start_time, end_time)
            thread["energy"] = segment_energy
            
            # Boost score for high energy moments
            if segment_energy > 0.5:
                thread["viral_score"] += segment_energy * 5
        
        # Sort by enhanced viral score
        conversation_threads.sort(key=lambda x: x["viral_score"], reverse=True)
        
        print(f"🎯 Found {len(conversation_threads)} meaningful conversation threads")
        return conversation_threads[:10]
    
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
                            thread_data, visual_data, audio_data):
        """Advanced short video creation with multi-speaker layout and effects"""
        print(f"🎬 Creating AI-optimized short: {output_path}")
        
        # Extract video clip
        video = VideoFileClip(video_path)
        clip = video.subclip(start_time, end_time)
        
        # Resize to 9:16 aspect ratio
        clip = clip.resize(height=1920)
        clip = clip.resize(width=1080)
        
        # Apply intelligent layout based on speakers
        if thread_data.get("is_multi_speaker", False):
            clip = self.create_dynamic_multi_speaker_layout(clip, thread_data, visual_data)
        else:
            clip = self.create_advanced_single_person(clip, visual_data)
        
        # Add dynamic background music
        clip = self.add_dynamic_music(clip, audio_data)
        
        # Add intelligent text overlay with speaker labels
        clip = self.add_speaker_aware_text(clip, thread_data)
        
        # Add professional transitions
        clip = self.add_professional_transitions(clip, thread_data)
        
        # Export with high quality
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac', 
                           verbose=False, logger=None, threads=4)
        
        clip.close()
        video.close()
    
    def create_dynamic_multi_speaker_layout(self, clip, thread_data, visual_data):
        """Dynamic multi-speaker layout with smart positioning"""
        speakers = thread_data.get("speakers", ["Speaker_A", "Speaker_B"])
        num_speakers = len(speakers)
        
        if num_speakers == 2:
            # Dynamic split-screen for 2 speakers
            return self.create_two_speaker_layout(clip, thread_data, visual_data)
        elif num_speakers > 2:
            # Picture-in-picture for 3+ speakers
            return self.create_picture_in_picture_layout(clip, thread_data, visual_data)
        else:
            # Single speaker fallback
            return self.create_advanced_single_person(clip, visual_data)
    
    def create_two_speaker_layout(self, clip, thread_data, visual_data):
        """Intelligent two-speaker split-screen with active speaker highlighting"""
        width = clip.w
        height = clip.h
        
        # Create split clips
        left_clip = clip.crop(x1=0, x2=width//2, y1=0, y2=height)
        right_clip = clip.crop(x1=width//2, x2=width, y1=0, y2=height)
        
        # Add subtle zoom to active speaker (simulate with slight resize)
        left_clip = left_clip.resize(1.05).set_position(('left', 'center'))
        right_clip = right_clip.resize(1.05).set_position(('right', 'center'))
        
        # Create speaker labels
        speaker_labels = self.create_speaker_labels(thread_data["speakers"])
        
        # Composite with labels
        final_clip = CompositeVideoClip([left_clip, right_clip] + speaker_labels, size=(1080, 1920))
        
        return final_clip
    
    def create_picture_in_picture_layout(self, clip, thread_data, visual_data):
        """Picture-in-picture layout for 3+ speakers"""
        # Main speaker (largest)
        main_clip = clip.crop(width=720, height=1280, x_center=clip.w/2, y_center=clip.h/2)
        main_clip = main_clip.set_position(('center', 'center'))
        
        # Secondary speakers (smaller insets)
        inset_clips = []
        positions = [(50, 50), (730, 50), (50, 1370), (730, 1370)]  # Corner positions
        
        for i, pos in enumerate(positions[:min(3, len(thread_data["speakers"]) - 1)]):
            inset = clip.crop(width=300, height=400, x_center=clip.w/4 * (i+1), y_center=clip.h/4 * (i+1))
            inset = inset.set_position(pos).resize(0.3)
            inset_clips.append(inset)
        
        # Add speaker labels
        speaker_labels = self.create_speaker_labels(thread_data["speakers"])
        
        # Composite all clips
        final_clip = CompositeVideoClip([main_clip] + inset_clips + speaker_labels, size=(1080, 1920))
        
        return final_clip
    
    def create_speaker_labels(self, speakers):
        """Create speaker label overlays"""
        labels = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i, speaker in enumerate(speakers[:5]):  # Max 5 speakers
            try:
                # Create label background
                label_bg = ColorClip(size=(200, 40), color=(0, 0, 0), duration=10)
                label_bg = label_bg.set_opacity(0.7)
                
                # Create text
                label_text = TextClip(speaker.replace('_', ' '), fontsize=20, color=colors[i % len(colors)])
                label_text = label_text.set_position(('center', 'center'))
                
                # Composite label
                label = CompositeVideoClip([label_bg, label_text])
                
                # Position label
                if i == 0:
                    label = label.set_position((50, 100))
                elif i == 1:
                    label = label.set_position((830, 100))
                else:
                    label = label.set_position((50, 200 + i * 50))
                
                labels.append(label)
            except Exception as e:
                print(f"⚠️ Could not create speaker label for {speaker}: {e}")
        
        return labels
    
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
    
    def add_speaker_aware_text(self, clip, thread_data):
        """Add text overlay with speaker attribution and context awareness"""
        text = thread_data.get("text", "")
        speakers = thread_data.get("speakers", [])
        
        # Break text into readable lines
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 30:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Create text clips with animation
        text_clips = []
        
        # Add speaker attribution if multi-speaker
        if len(speakers) > 1:
            speaker_text = f"{len(speakers)} Speakers"
            try:
                speaker_clip = TextClip(speaker_text, fontsize=25, color='#4ECDC4', font='Arial-Bold')
                speaker_clip = speaker_clip.set_position(('center', 80)).set_duration(clip.duration)
                text_clips.append(speaker_clip)
            except:
                pass
        
        # Add main content text
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            try:
                txt_clip = TextClip(line, fontsize=40, color='white', font='Arial-Bold')
                txt_clip = txt_clip.set_position(('center', 150 + i * 50))
                
                # Staggered animation for each line
                txt_clip = txt_clip.set_start(i * 0.2).set_duration(clip.duration - i * 0.2)
                txt_clip = txt_clip.fadein(0.3).fadeout(0.3)
                
                text_clips.append(txt_clip)
            except Exception as e:
                print(f"⚠️ Text creation failed: {e}")
        
        # Background for text
        if text_clips:
            try:
                bg_height = len(lines) * 50 + 40
                if len(speakers) > 1:
                    bg_height += 30
                    
                bg_clip = ColorClip(size=(900, bg_height), color=(0, 0, 0), duration=clip.duration)
                bg_clip = bg_clip.set_position(('center', 70)).set_opacity(0.8)
                text_clips.insert(0, bg_clip)
            except:
                pass
        
        # Composite
        try:
            final_clip = CompositeVideoClip([clip] + text_clips)
            return final_clip
        except Exception as e:
            print(f"⚠️ Text overlay failed: {e}")
            return clip
    
    def add_professional_transitions(self, clip, thread_data):
        """Add professional transitions based on content type"""
        try:
            # Base fade transitions
            clip = clip.fadein(0.5).fadeout(0.5)
            
            # Add zoom effect for high-engagement content
            if thread_data.get("engagement_score", 0) > 5:
                # Subtle zoom in the middle
                zoom_clip = clip.resize(lambda t: 1 + 0.05 * np.sin(t * 2))
                clip = zoom_clip
            
            # Add speed effect for high-energy moments
            if thread_data.get("energy", 0) > 1:
                # Slight speed ramp
                if clip.duration > 10:
                    # Speed up middle section
                    first_part = clip.subclip(0, 2)
                    middle_part = clip.subclip(2, clip.duration - 2).speedx(1.1)
                    last_part = clip.subclip(clip.duration - 2, clip.duration)
                    clip = concatenate_videoclips([first_part, middle_part, last_part])
            
            return clip
        except Exception as e:
            print(f"⚠️ Professional transitions failed: {e}")
            return clip.fadein(0.3).fadeout(0.3)
