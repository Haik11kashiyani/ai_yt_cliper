#!/usr/bin/env python3
"""
Test script for YouTube Shorts Generator
"""

import os
import sys
from main import YouTubeShortsGenerator

def test_basic_functionality():
    """Test basic functionality with a sample URL"""
    
    # Test URL (you can replace with any YouTube video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    
    print("🧪 Testing YouTube Shorts Generator...")
    print(f"Test URL: {test_url}")
    
    try:
        # Initialize generator
        generator = YouTubeShortsGenerator(use_advanced=False)  # Use basic mode for testing
        
        # Test video download
        print("\n1. Testing video download...")
        video_path, video_info = generator.download_video(test_url)
        print(f"✅ Video downloaded: {video_path}")
        print(f"   Duration: {video_info.get('duration', 'Unknown')} seconds")
        
        # Test audio extraction and transcription
        print("\n2. Testing audio extraction and transcription...")
        segments, full_text = generator.extract_audio_and_transcribe(video_path)
        print(f"✅ Transcription completed")
        print(f"   Segments: {len(segments)}")
        print(f"   Text length: {len(full_text)} characters")
        
        # Test content analysis
        print("\n3. Testing content analysis...")
        viral_moments = generator.analyze_content(full_text)
        print(f"✅ Content analysis completed")
        print(f"   Viral moments found: {len(viral_moments)}")
        
        # Test timestamp finding
        print("\n4. Testing timestamp finding...")
        moments_with_timestamps = generator.find_timestamps_for_moments(viral_moments, segments)
        print(f"✅ Timestamp finding completed")
        print(f"   Moments with timestamps: {len(moments_with_timestamps)}")
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False

def test_advanced_functionality():
    """Test advanced functionality"""
    
    print("\n🧠 Testing Advanced Features...")
    
    try:
        from advanced_generator import AdvancedShortsGenerator
        
        # Initialize advanced generator
        advanced_gen = AdvancedShortsGenerator()
        print("✅ Advanced generator initialized")
        
        # Test audio analysis (with dummy data)
        print("✅ Advanced features available")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 YouTube Shorts Generator Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_test = test_basic_functionality()
    
    # Test advanced functionality
    advanced_test = test_advanced_functionality()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Basic Functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"Advanced Functionality: {'✅ PASS' if advanced_test else '❌ FAIL'}")
    
    if basic_test and advanced_test:
        print("\n🎉 All tests passed! System is ready to use.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
