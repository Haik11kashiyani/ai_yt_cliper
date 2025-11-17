#!/usr/bin/env python3
"""
Video Manager for YouTube Shorts Generator
Handles finding, organizing, and uploading generated shorts
"""

import os
import json
import glob
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class VideoManager:
    """Manages generated short videos and their metadata"""
    
    def __init__(self, output_dir: str = "generated_shorts"):
        self.output_dir = output_dir
        self.metadata_file = os.path.join(output_dir, "shorts_metadata.json")
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def find_generated_shorts(self) -> List[Dict]:
        """Find all generated short videos and their metadata"""
        shorts = []
        
        # Find all MP4 files
        video_files = glob.glob(os.path.join(self.output_dir, "*.mp4"))
        
        for video_path in video_files:
            filename = os.path.basename(video_path)
            
            # Get file info
            stat = os.stat(video_path)
            file_size = stat.st_size
            created_time = datetime.fromtimestamp(stat.st_ctime)
            
            # Generate unique ID
            file_hash = self._generate_file_hash(video_path)
            
            short_info = {
                "filename": filename,
                "path": video_path,
                "file_size": file_size,
                "created_at": created_time.isoformat(),
                "file_hash": file_hash,
                "download_url": f"https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}/artifacts/{filename}"
            }
            
            # Try to load additional metadata from JSON if exists
            metadata_path = video_path.replace('.mp4', '_metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    additional_metadata = json.load(f)
                    short_info.update(additional_metadata)
            
            shorts.append(short_info)
        
        # Sort by creation time (newest first)
        shorts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return shorts
    
    def _generate_file_hash(self, file_path: str) -> str:
        """Generate MD5 hash for file identification"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def save_short_metadata(self, short_data: Dict, video_path: str):
        """Save metadata for a generated short"""
        metadata_path = video_path.replace('.mp4', '_metadata.json')
        
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "text": short_data.get("text", ""),
            "speakers": short_data.get("speakers", []),
            "is_multi_speaker": short_data.get("is_multi_speaker", False),
            "engagement_score": short_data.get("engagement_score", 0),
            "viral_score": short_data.get("viral_score", 0),
            "duration": short_data.get("end_time", 0) - short_data.get("start_time", 0),
            "original_url": short_data.get("original_url", ""),
            "start_time": short_data.get("start_time", 0),
            "end_time": short_data.get("end_time", 0)
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def create_summary_report(self) -> str:
        """Create a summary report of all generated shorts"""
        shorts = self.find_generated_shorts()
        
        if not shorts:
            return "No generated shorts found."
        
        report = []
        report.append("# 🎬 Generated YouTube Shorts Summary")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total shorts: {len(shorts)}")
        report.append("")
        
        for i, short in enumerate(shorts, 1):
            report.append(f"## {i}. {short['filename']}")
            report.append(f"- **Size**: {short['file_size']:,} bytes")
            report.append(f"- **Created**: {short['created_at']}")
            report.append(f"- **Hash**: `{short['file_hash'][:8]}...`")
            
            if 'text' in short:
                report.append(f"- **Text**: {short['text'][:100]}...")
            
            if 'speakers' in short:
                speakers_text = f"{len(short['speakers'])} speakers" if short.get('is_multi_speaker') else "1 speaker"
                report.append(f"- **Speakers**: {speakers_text}")
            
            if 'engagement_score' in short:
                report.append(f"- **Engagement Score**: {short['engagement_score']:.1f}")
            
            if 'viral_score' in short:
                report.append(f"- **Viral Score**: {short['viral_score']:.1f}")
            
            if 'duration' in short:
                report.append(f"- **Duration**: {short['duration']:.1f}s")
            
            report.append("")
        
        # Save report
        report_path = os.path.join(self.output_dir, "SHORTS_SUMMARY.md")
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        return report_path
    
    def get_download_instructions(self) -> str:
        """Get instructions for downloading shorts from GitHub"""
        return """
# 📥 How to Download Generated Shorts

## From GitHub Actions Artifacts:

1. Go to your repository's **Actions** tab
2. Click on the latest workflow run
3. Look for the **test-shorts** artifact
4. Click **Download** to get all generated shorts

## Direct Download URLs:

Each short video has a direct download URL in the format:
```
https://github.com/OWNER/REPO/actions/runs/RUN_ID/artifacts/FILENAME
```

## Local Development:

If running locally, generated shorts are saved in:
```
generated_shorts/
├── short_1.mp4
├── short_1_metadata.json
├── short_2.mp4
├── short_2_metadata.json
└── SHORTS_SUMMARY.md
```

## API Access:

You can access shorts programmatically via the GitHub API:
```bash
curl -H "Authorization: token YOUR_TOKEN" \\
  https://api.github.com/repos/OWNER/REPO/actions/artifacts
```
"""
    
    def cleanup_old_shorts(self, keep_count: int = 10):
        """Clean up old shorts, keeping only the most recent ones"""
        shorts = self.find_generated_shorts()
        
        if len(shorts) <= keep_count:
            return
        
        # Remove oldest shorts
        shorts_to_remove = shorts[keep_count:]
        
        for short in shorts_to_remove:
            try:
                os.remove(short['path'])
                # Remove metadata file if exists
                metadata_path = short['path'].replace('.mp4', '_metadata.json')
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                print(f"🗑️ Removed old short: {short['filename']}")
            except Exception as e:
                print(f"⚠️ Could not remove {short['filename']}: {e}")

def integrate_with_main_generator():
    """Integration function to be called from main.py"""
    def save_short_metadata_wrapper(short_data, output_path):
        """Wrapper to save metadata when shorts are generated"""
        manager = VideoManager()
        manager.save_short_metadata(short_data, output_path)
    
    return save_short_metadata_wrapper

if __name__ == "__main__":
    # Test the video manager
    manager = VideoManager()
    
    print("🔍 Searching for generated shorts...")
    shorts = manager.find_generated_shorts()
    
    if shorts:
        print(f"✅ Found {len(shorts)} generated shorts:")
        for short in shorts:
            print(f"  - {short['filename']} ({short['file_size']:,} bytes)")
        
        print("\n📊 Creating summary report...")
        report_path = manager.create_summary_report()
        print(f"✅ Summary report saved to: {report_path}")
        
        print("\n📋 Download instructions:")
        print(manager.get_download_instructions())
    else:
        print("❌ No generated shorts found.")
        print("💡 Run the generator first: python main.py --url 'YOUTUBE_URL'")
