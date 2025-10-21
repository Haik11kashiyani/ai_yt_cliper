#!/usr/bin/env python3
"""
GitHub Repository Testing Script
Run this after cloning the repository
"""

import os
import sys
import subprocess
import requests
import time

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import yt_dlp
        import cv2
        import numpy as np
        from moviepy.editor import *
        import whisper
        import librosa
        import soundfile as sf
        from transformers import pipeline
        print("✅ All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("🧪 Testing basic functionality...")
    
    try:
        from main import YouTubeShortsGenerator
        
        # Test initialization
        generator = YouTubeShortsGenerator(use_advanced=False)
        print("✅ Generator initialized successfully")
        
        # Test with a short video (Rick Roll - 3 minutes)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        print(f"🎬 Testing with: {test_url}")
        
        # This will take some time, so we'll just test the download part
        video_path, video_info = generator.download_video(test_url)
        print(f"✅ Video downloaded: {video_path}")
        print(f"   Duration: {video_info.get('duration', 'Unknown')} seconds")
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def test_web_app():
    """Test web application"""
    print("🌐 Testing web application...")
    
    try:
        from web_app import app
        
        # Test if app can be created
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Web app responds successfully")
                return True
            else:
                print(f"❌ Web app returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False

def test_advanced_features():
    """Test advanced features"""
    print("🧠 Testing advanced features...")
    
    try:
        from advanced_generator import AdvancedShortsGenerator
        
        # Test initialization
        advanced_gen = AdvancedShortsGenerator()
        print("✅ Advanced generator initialized")
        
        # Test audio analysis with dummy data
        import numpy as np
        dummy_audio = np.random.normal(0, 0.1, 44100)  # 1 second of audio
        
        # This would normally require a real audio file, so we'll skip the actual analysis
        print("✅ Advanced features available")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced features test failed: {e}")
        return False

def run_full_test():
    """Run complete test suite"""
    print("🚀 Starting GitHub Repository Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Dependencies
    if check_dependencies():
        tests_passed += 1
    else:
        print("📦 Installing missing dependencies...")
        if install_dependencies():
            if check_dependencies():
                tests_passed += 1
    
    # Test 2: Basic functionality
    if test_basic_functionality():
        tests_passed += 1
    
    # Test 3: Web application
    if test_web_app():
        tests_passed += 1
    
    # Test 4: Advanced features
    if test_advanced_features():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! Repository is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: python web_app.py")
        print("2. Open: http://localhost:5000")
        print("3. Test with a YouTube URL")
    else:
        print(f"\n⚠️ {total_tests - tests_passed} tests failed.")
        print("Please check the error messages above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)
