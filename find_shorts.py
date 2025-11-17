#!/usr/bin/env python3
"""
Find and display information about generated YouTube shorts
"""

import os
import json
import glob
from datetime import datetime
from video_manager import VideoManager

def main():
    print("🔍 Searching for generated YouTube shorts...")
    print("=" * 50)
    
    manager = VideoManager()
    shorts = manager.find_generated_shorts()
    
    if not shorts:
        print("❌ No generated shorts found.")
        print("\n💡 To generate shorts, run:")
        print("   python main.py --url 'YOUTUBE_URL'")
        return
    
    print(f"✅ Found {len(shorts)} generated shorts:\n")
    
    # Display detailed information
    for i, short in enumerate(shorts, 1):
        print(f"🎬 {i}. {short['filename']}")
        print(f"   📁 Path: {short['path']}")
        print(f"   📊 Size: {short['file_size']:,} bytes")
        print(f"   📅 Created: {short['created_at']}")
        print(f"   🔑 Hash: {short['file_hash'][:16]}...")
        
        if 'text' in short:
            print(f"   💬 Text: {short['text'][:80]}...")
        
        if 'speakers' in short:
            speakers_text = f"{len(short['speakers'])} speakers" if short.get('is_multi_speaker') else "1 speaker"
            print(f"   👥 Speakers: {speakers_text}")
        
        if 'engagement_score' in short:
            print(f"   📈 Engagement: {short['engagement_score']:.1f}")
        
        if 'viral_score' in short:
            print(f"   🚀 Viral Score: {short['viral_score']:.1f}")
        
        if 'duration' in short:
            print(f"   ⏱️ Duration: {short['duration']:.1f}s")
        
        print()
    
    # Create summary
    print("📋 Summary Report:")
    print(f"   Total shorts: {len(shorts)}")
    print(f"   Total size: {sum(s['file_size'] for s in shorts):,} bytes")
    print(f"   Latest: {shorts[0]['filename']}")
    print(f"   Oldest: {shorts[-1]['filename']}")
    
    # Check for metadata files
    metadata_files = glob.glob("generated_shorts/*_metadata.json")
    print(f"   Metadata files: {len(metadata_files)}")
    
    # Show download instructions
    print("\n" + "=" * 50)
    print("📥 How to Download/Share Shorts:")
    print("=" * 50)
    
    print("\n🌐 From GitHub Actions:")
    print("1. Go to your repository's 'Actions' tab")
    print("2. Click on the latest workflow run")
    print("3. Download the 'test-shorts' artifact")
    
    print("\n💻 Local Files:")
    print("   Shorts are saved in: generated_shorts/")
    print("   Each video has a matching _metadata.json file")
    
    print("\n📊 Summary Report:")
    report_path = os.path.join("generated_shorts", "SHORTS_SUMMARY.md")
    if os.path.exists(report_path):
        print(f"   View detailed report: {report_path}")
    else:
        print("   Generate report: python video_manager.py")
    
    print("\n🔗 API Access:")
    print("   Use GitHub API to download artifacts programmatically")
    print("   See video_manager.py for implementation details")
    
    # Show file structure
    print("\n📁 File Structure:")
    print("   generated_shorts/")
    print("   ├── short_1.mp4")
    print("   ├── short_1_metadata.json")
    print("   ├── short_2.mp4")
    print("   ├── short_2_metadata.json")
    print("   └── SHORTS_SUMMARY.md")
    
    print(f"\n🎯 Ready to share! All shorts are optimized for social media.")

if __name__ == "__main__":
    main()
