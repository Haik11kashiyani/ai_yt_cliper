import os
import sys
import argparse
import yt_dlp
import cv2
import numpy as np
from moviepy.editor import *
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper not available, using fallback mode")
import librosa
import soundfile as sf
from transformers import pipeline
import json
from datetime import timedelta
import re
from advanced_generator import AdvancedShortsGenerator

class YouTubeShortsGenerator:
    def __init__(self, use_advanced=True):
        if WHISPER_AVAILABLE:
            try:
                self.model = whisper.load_model("base")
            except Exception as e:
                print(f"⚠️ Whisper model loading failed: {e}")
                print("🔄 Using fallback mode...")
                self.model = None
        else:
            self.model = None
        
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.use_advanced = use_advanced
        if use_advanced:
            self.advanced_generator = AdvancedShortsGenerator()
        
    def download_video(self, url, demo_mode=False):
        """YouTube video download करता है"""
        print("📥 Video downloading...")
        
        if demo_mode:
            print("🎭 Demo mode: Creating mock video data...")
            # Create a mock video file for testing
            mock_video_path = "temp_video.mp4"
            
            # Create a simple test video using MoviePy without TextClip to avoid ImageMagick dependency
            from moviepy.editor import ColorClip
            
            # Create a simple colored video with gradient effect
            video_clip = ColorClip(size=(1280, 720), color=(100, 150, 200), duration=30)
            
            # Write the video without text overlay to avoid ImageMagick dependency
            video_clip.write_videofile(mock_video_path, verbose=False, logger=None)
            
            mock_info = {
                'duration': 30,
                'title': 'Demo Video',
                'ext': 'mp4'
            }
            
            return mock_video_path, mock_info
        
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]/best[height<=720]/best',
            'outtmpl': 'temp_video.%(ext)s',
            'extractaudio': False,
            'noplaylist': True,
            'cookiesfrombrowser': None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': 1,
            'max_sleep_interval': 5,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = f"temp_video.{info['ext']}"
                
                # Ensure we have a valid video format
                if info['ext'] not in ['mp4', 'webm', 'mkv']:
                    print(f"⚠️ Unsupported format: {info['ext']}, trying to convert...")
                    # Try to download in mp4 format
                    ydl_opts['format'] = 'best[ext=mp4]/best'
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                        info = ydl2.extract_info(url, download=True)
                        video_path = f"temp_video.{info['ext']}"
                
                return video_path, info
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("🔄 Trying alternative download method...")
            
            # Alternative method with different options
            ydl_opts_alt = {
                'format': 'worst[ext=mp4]/worst',
                'outtmpl': 'temp_video.%(ext)s',
                'extractaudio': False,
                'noplaylist': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts_alt) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_path = f"temp_video.{info['ext']}"
                    return video_path, info
            except Exception as e2:
                print(f"❌ Alternative download also failed: {e2}")
                raise Exception(f"Could not download video: {e2}")
    
    def extract_audio_and_transcribe(self, video_path):
        """Audio extract करके transcription करता है"""
        print("🎵 Audio extracting और transcribing...")
        
        # Audio extract करना
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        if self.model is not None:
            try:
                # Transcription
                result = self.model.transcribe(audio_path)
                
                # Timestamps के साथ segments
                segments = []
                for segment in result["segments"]:
                    segments.append({
                        "start": segment["start"],
                        "end": segment["end"],
                        "text": segment["text"].strip()
                    })
                
                return segments, result["text"]
            except Exception as e:
                print(f"⚠️ Whisper transcription failed: {e}")
                print("🔄 Using fallback transcription...")
        else:
            print("🔄 Whisper not available, using fallback transcription...")
        
        # Fallback: Create dummy segments
        duration = video.duration
        segments = []
        for i in range(0, int(duration), 10):  # Every 10 seconds
            segments.append({
                "start": i,
                "end": min(i + 10, duration),
                "text": f"Segment {i//10 + 1} - Video content"
            })
        
        return segments, "Video transcription placeholder"
    
    def analyze_content(self, full_text):
        """Content analysis करके viral moments identify करता है"""
        print("🔍 Content analyzing...")
        
        # Text को chunks में divide करना
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Key phrases और emotional content detect करना
        viral_keywords = [
            "amazing", "incredible", "unbelievable", "shocking", "wow", "omg",
            "you won't believe", "this will blow your mind", "wait for it",
            "अद्भुत", "अविश्वसनीय", "चौंकाने वाला", "वाह", "क्या बात है"
        ]
        
        viral_moments = []
        for i, sentence in enumerate(sentences):
            if any(keyword.lower() in sentence.lower() for keyword in viral_keywords):
                viral_moments.append({
                    "sentence": sentence,
                    "index": i,
                    "score": len([k for k in viral_keywords if k.lower() in sentence.lower()])
                })
        
        # Score के basis पर sort करना
        viral_moments.sort(key=lambda x: x["score"], reverse=True)
        
        return viral_moments[:10]  # Top 10 viral moments
    
    def find_timestamps_for_moments(self, viral_moments, segments):
        """Viral moments के लिए timestamps find करता है"""
        print("⏰ Finding timestamps...")
        
        moments_with_timestamps = []
        
        for moment in viral_moments:
            sentence = moment["sentence"]
            
            # Best matching segment find करना
            best_match = None
            best_score = 0
            
            for segment in segments:
                # Text similarity check
                words_in_sentence = set(sentence.lower().split())
                words_in_segment = set(segment["text"].lower().split())
                
                if words_in_sentence and words_in_segment:
                    similarity = len(words_in_sentence.intersection(words_in_segment)) / len(words_in_sentence.union(words_in_segment))
                    
                    if similarity > best_score and similarity > 0.3:
                        best_score = similarity
                        best_match = segment
            
            if best_match:
                moments_with_timestamps.append({
                    "text": sentence,
                    "start": best_match["start"],
                    "end": best_match["end"],
                    "score": moment["score"]
                })
        
        return moments_with_timestamps
    
    def detect_faces_and_people(self, video_path, start_time, end_time):
        """Video में faces detect करता है"""
        print("👥 Detecting faces...")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Start और end frame calculate करना
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        
        # Face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        face_count = 0
        frame_count = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        while cap.isOpened() and frame_count < (end_frame - start_frame):
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > face_count:
                face_count = len(faces)
            
            frame_count += 1
        
        cap.release()
        return face_count
    
    def create_short_video(self, video_path, start_time, end_time, output_path, text_content, face_count):
        """Individual short video create करता है"""
        print(f"🎬 Creating short: {output_path}")
        
        # Video clip extract करना
        video = VideoFileClip(video_path)
        clip = video.subclip(start_time, end_time)
        
        # Aspect ratio को 9:16 (vertical) में convert करना
        clip = clip.resize(height=1920)
        
        # Width को 1080 में set करना (9:16 ratio)
        clip = clip.resize(width=1080)
        
        # Face count के basis पर layout decide करना
        if face_count > 1:
            # Multiple people - side by side layout
            clip = self.create_side_by_side_layout(clip)
        else:
            # Single person - center crop
            clip = self.create_center_crop(clip)
        
        # Background music add करना (5-6% volume)
        clip = self.add_background_music(clip)
        
        # Text overlay add करना
        clip = self.add_text_overlay(clip, text_content)
        
        # Final touches
        clip = clip.fadein(0.5).fadeout(0.5)
        
        # Export करना
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
        
        # Memory cleanup
        clip.close()
        video.close()
    
    def create_side_by_side_layout(self, clip):
        """Multiple people के लिए side by side layout"""
        # Video को दो parts में divide करना
        width = clip.w
        height = clip.h
        
        # Left और right halves
        left_clip = clip.crop(x1=0, x2=width//2, y1=0, y2=height)
        right_clip = clip.crop(x1=width//2, x2=width, y1=0, y2=height)
        
        # Side by side compose करना
        final_clip = CompositeVideoClip([left_clip.set_position(('left', 'center')), 
                                       right_clip.set_position(('right', 'center'))], 
                                      size=(1080, 1920))
        
        return final_clip
    
    def create_center_crop(self, clip):
        """Single person के लिए center crop"""
        # Center crop करना
        clip = clip.crop(width=1080, height=1920, x_center=clip.w/2, y_center=clip.h/2)
        return clip
    
    def add_background_music(self, clip):
        """Background music add करना (5-6% volume)"""
        try:
            # Simple background music generation
            duration = clip.duration
            
            # Generate a simple beat
            audio_array = np.random.normal(0, 0.1, int(44100 * duration))
            
            # Create audio clip
            audio_clip = AudioClip(lambda t: audio_array[int(t * 44100)], duration=duration)
            
            # Volume को 5-6% में set करना
            audio_clip = audio_clip.volumex(0.05)
            
            # Original audio के साथ mix करना
            if clip.audio:
                final_audio = CompositeAudioClip([clip.audio, audio_clip])
                clip = clip.set_audio(final_audio)
            else:
                clip = clip.set_audio(audio_clip)
                
        except Exception as e:
            print(f"Music addition failed: {e}")
        
        return clip
    
    def add_text_overlay(self, clip, text):
        """Text overlay add करना"""
        try:
            # Try to use TextClip if ImageMagick is available
            from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
            
            # Text को lines में break करना
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= 30:  # Max 30 characters per line
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Text clips create करना
            text_clips = []
            for i, line in enumerate(lines):
                txt_clip = TextClip(line, fontsize=50, color='white', font='Arial-Bold')
                txt_clip = txt_clip.set_position(('center', 100 + i * 60)).set_duration(clip.duration)
                text_clips.append(txt_clip)
            
            # Background for text
            if text_clips:
                bg_clip = ColorClip(size=(1080, len(lines) * 60 + 40), color=(0, 0, 0), duration=clip.duration)
                bg_clip = bg_clip.set_position(('center', 80)).set_opacity(0.7)
                text_clips.insert(0, bg_clip)
            
            # Composite करना
            final_clip = CompositeVideoClip([clip] + text_clips)
            return final_clip
            
        except Exception as e:
            print(f"⚠️ Text overlay failed (ImageMagick not available): {e}")
            print("🔄 Using video without text overlay...")
            # Return the original clip without text overlay
            return clip
    
    def generate_shorts(self, url, demo_mode=False):
        """Main function - सभी shorts generate करता है"""
        print("🚀 Starting YouTube Shorts Generation...")
        
        # Step 1: Video download
        video_path, video_info = self.download_video(url, demo_mode=demo_mode)
        
        # Step 2: Audio extract और transcription
        segments, full_text = self.extract_audio_and_transcribe(video_path)
        
        if self.use_advanced:
            # Advanced analysis
            print("🧠 Using advanced analysis...")
            
            # Audio features analysis
            audio_path = "temp_audio.wav"
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            
            audio_features = self.advanced_generator.analyze_audio_features(audio_path)
            
            # Advanced content analysis
            viral_moments = self.advanced_generator.advanced_content_analysis(segments, audio_features)
            
            # Step 3: Shorts generate करना
            output_dir = "generated_shorts"
            os.makedirs(output_dir, exist_ok=True)
            
            generated_shorts = []
            
            for i, moment in enumerate(viral_moments[:5]):  # Top 5 shorts
                start_time = max(0, moment["start"] - 2)  # 2 seconds before
                end_time = min(video_info.get('duration', 3600), moment["end"] + 2)  # 2 seconds after
                
                # Visual analysis
                visual_data = self.advanced_generator.detect_visual_interest(video_path, start_time, end_time)
                
                # Advanced short video create करना
                output_path = f"{output_dir}/short_{i+1}.mp4"
                self.advanced_generator.create_advanced_short(
                    video_path, start_time, end_time, output_path, 
                    moment["text"], visual_data, audio_features
                )
                
                generated_shorts.append({
                    "path": output_path,
                    "text": moment["text"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "face_count": visual_data["max_faces"],
                    "viral_score": moment["viral_score"],
                    "sentiment": moment["sentiment"]["label"],
                    "emotion": moment["emotion"]["label"]
                })
            
            # Cleanup
            os.remove(audio_path)
            
        else:
            # Basic analysis (original method)
            viral_moments = self.analyze_content(full_text)
            moments_with_timestamps = self.find_timestamps_for_moments(viral_moments, segments)
            
            output_dir = "generated_shorts"
            os.makedirs(output_dir, exist_ok=True)
            
            generated_shorts = []
            
            for i, moment in enumerate(moments_with_timestamps[:5]):
                start_time = max(0, moment["start"] - 2)
                end_time = min(video_info.get('duration', 3600), moment["end"] + 2)
                
                face_count = self.detect_faces_and_people(video_path, start_time, end_time)
                
                output_path = f"{output_dir}/short_{i+1}.mp4"
                self.create_short_video(video_path, start_time, end_time, output_path, moment["text"], face_count)
                
                generated_shorts.append({
                    "path": output_path,
                    "text": moment["text"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "face_count": face_count
                })
        
        # Cleanup
        os.remove(video_path)
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        
        print(f"✅ Generated {len(generated_shorts)} shorts in '{output_dir}' folder!")
        return generated_shorts

def main():
    parser = argparse.ArgumentParser(description='YouTube Long Form to Viral Shorts Generator')
    parser.add_argument('--url', required=True, help='YouTube video URL')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (no actual download)')
    
    args = parser.parse_args()
    
    generator = YouTubeShortsGenerator()
    shorts = generator.generate_shorts(args.url, demo_mode=args.demo)
    
    print("\n📊 Generated Shorts Summary:")
    for i, short in enumerate(shorts, 1):
        print(f"{i}. {short['text'][:50]}...")
        print(f"   Duration: {short['end_time'] - short['start_time']:.1f}s")
        print(f"   Faces detected: {short['face_count']}")
        print(f"   File: {short['path']}\n")

if __name__ == "__main__":
    main()
