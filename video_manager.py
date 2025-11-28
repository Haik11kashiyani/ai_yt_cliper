import os
import yt_dlp
from config import VIDEO_DIR

class VideoManager:
    def __init__(self):
        self.video_dir = VIDEO_DIR
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)

    def download_video(self, url):
        """
        Downloads video using yt-dlp (Most Reliable Method)
        """
        print(f"⬇️ Starting download: {url}")
        
        # Clean up old files
        self.cleanup()

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.video_dir, '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"✅ Download complete: {filename}")
                return filename
        except Exception as e:
            print(f"❌ Download Failed: {str(e)}")
            raise e

    def cleanup(self):
        """Removes old video files to save space"""
        for f in os.listdir(self.video_dir):
            if f.endswith((".mp4", ".mkv", ".webm")):
                try:
                    os.remove(os.path.join(self.video_dir, f))
                except:
                    pass
