# 🧪 GitHub Repository Testing Guide

## 📋 Testing Methods After GitHub Upload

### **Method 1: GitHub Actions (Automated Testing)**

1. **Go to your GitHub repository**
2. **Click on "Actions" tab**
3. **Select "Test YouTube Shorts Generator" workflow**
4. **Click "Run workflow"**
5. **Enter a test YouTube URL** (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
6. **Click "Run workflow"**
7. **Wait for completion** (5-10 minutes)
8. **Download generated shorts** from artifacts

### **Method 2: Local Testing (After Clone)**

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/clip_yt_ai.git
cd clip_yt_ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run comprehensive test
python github_test.py

# 4. Run basic test
python test.py

# 5. Test web application
python web_app.py
# Open http://localhost:5000 in browser

# 6. Test with sample video
python main.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### **Method 3: GitHub Codespaces (Cloud Testing)**

1. **Go to your GitHub repository**
2. **Click "Code" button**
3. **Select "Codespaces" tab**
4. **Click "Create codespace on main"**
5. **Wait for environment setup** (2-3 minutes)
6. **Run test commands in terminal:**
   ```bash
   python github_test.py
   python web_app.py
   ```
7. **Open forwarded port 5000** for web interface

### **Method 4: Docker Testing**

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run tests
RUN python github_test.py

# Start web application
CMD ["python", "web_app.py"]
EOF

# Build and run
docker build -t youtube-shorts-generator .
docker run -p 5000:5000 youtube-shorts-generator
```

## 🎯 What Each Test Checks

### **Basic Tests:**
- ✅ Dependencies installation
- ✅ Python imports
- ✅ Video download functionality
- ✅ Audio extraction
- ✅ Transcription
- ✅ Content analysis
- ✅ Video generation

### **Advanced Tests:**
- ✅ Emotion detection
- ✅ Sentiment analysis
- ✅ Audio features analysis
- ✅ Visual interest detection
- ✅ Viral score calculation
- ✅ Advanced video editing

### **Web Interface Tests:**
- ✅ Flask app startup
- ✅ Web interface loading
- ✅ URL validation
- ✅ Progress tracking
- ✅ File download

## 🚨 Common Issues & Solutions

### **Issue 1: FFmpeg not found**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### **Issue 2: Memory issues**
```python
# Reduce video quality in main.py
ydl_opts = {
    'format': 'worst[height<=480]',  # Lower quality
}
```

### **Issue 3: Model download issues**
```bash
# Clear cache
rm -rf ~/.cache/whisper
rm -rf ~/.cache/huggingface
```

### **Issue 4: Permission errors**
```bash
# Linux/Mac
chmod +x *.py
chmod +x *.sh

# Windows
# Run as administrator
```

## 📊 Expected Test Results

### **Successful Test Output:**
```
🚀 Starting GitHub Repository Test Suite
============================================================
🔍 Checking dependencies...
✅ All dependencies imported successfully
📦 Installing dependencies...
✅ Dependencies installed successfully
🧪 Testing basic functionality...
✅ Generator initialized successfully
🎬 Testing with: https://www.youtube.com/watch?v=dQw4w9WgXcQ
✅ Video downloaded: temp_video.mp4
   Duration: 212 seconds
🌐 Testing web application...
✅ Web app responds successfully
🧠 Testing advanced features...
✅ Advanced generator initialized
✅ Advanced features available

============================================================
📊 Test Results:
Tests Passed: 4/4
Success Rate: 100.0%

🎉 All tests passed! Repository is ready to use.

🚀 Next steps:
1. Run: python web_app.py
2. Open: http://localhost:5000
3. Test with a YouTube URL
```

## 🎬 Testing with Real Videos

### **Recommended Test Videos:**
1. **Short videos (1-5 minutes):**
   - `https://www.youtube.com/watch?v=dQw4w9WgXcQ` (Rick Roll)
   - `https://www.youtube.com/watch?v=jNQXAC9IVRw` (Me at the zoo)

2. **Medium videos (5-15 minutes):**
   - Any educational or tutorial video
   - Interview or podcast clips

3. **Long videos (15+ minutes):**
   - Documentary clips
   - Long-form content

### **Test Scenarios:**
- ✅ Single person talking
- ✅ Multiple people conversation
- ✅ Music videos
- ✅ Educational content
- ✅ Hindi/English mixed content

## 🔧 Performance Testing

### **Test with different video lengths:**
```bash
# Short video (2-3 minutes)
python main.py --url "SHORT_VIDEO_URL"

# Medium video (10-15 minutes)
python main.py --url "MEDIUM_VIDEO_URL"

# Long video (30+ minutes)
python main.py --url "LONG_VIDEO_URL"
```

### **Monitor system resources:**
- CPU usage during processing
- RAM usage (should be < 4GB)
- Disk space for temporary files
- Processing time per minute of video

## 📱 Mobile Testing

### **Test web interface on mobile:**
1. **Run web app:** `python web_app.py`
2. **Get local IP:** `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
3. **Access from mobile:** `http://YOUR_IP:5000`
4. **Test mobile interface responsiveness**

## 🚀 Production Testing

### **Before deploying to production:**
1. **Run all tests:** `python github_test.py`
2. **Test with multiple videos**
3. **Check error handling**
4. **Verify file cleanup**
5. **Test concurrent users**
6. **Monitor resource usage**

---

**Happy Testing! 🧪✨**
