from moviepy.editor import VideoFileClip, vfx
from speaker_analyzer import SpeakerAnalyzer
import os

class AdvancedVideoGenerator:
    def __init__(self):
        self.analyzer = SpeakerAnalyzer()

    def create_short(self, video_path, start_time, end_time, output_path):
        print(f"🎬 Creating short: {start_time} to {end_time}")
        
        try:
            # 1. Load Video
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            
            # 2. Analyze where the face is
            center_x_ratio = self.analyzer.detect_primary_speaker(video_path)
            
            # 3. Calculate Crop Coordinates (9:16 Aspect Ratio)
            w, h = clip.size
            target_ratio = 9 / 16
            target_width = int(h * target_ratio)
            
            # Ensure crop box stays within video bounds
            x_center = int(w * center_x_ratio)
            x1 = max(0, x_center - (target_width // 2))
            x2 = x1 + target_width
            
            if x2 > w:
                x2 = w
                x1 = x2 - target_width

            # 4. Apply Crop and Resize
            final_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h)
            final_clip = final_clip.resize(height=1920) # High Quality
            
            # 5. Write File
            final_clip.write_videofile(
                output_path, 
                codec='libx264', 
                audio_codec='aac',
                fps=24,
                preset='fast'
            )
            
            clip.close()
            final_clip.close()
            return output_path

        except Exception as e:
            print(f"❌ Error generating short: {e}")
            return None
