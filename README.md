# YouTube Long Form to Viral Shorts Automation

## Features
- YouTube video download और analysis
- AI-powered content analysis और key moments detection
- Automated shorts generation with proper cropping
- Background music integration (5-6% volume)
- Multiple person detection और side-by-side layout
- Web interface for easy usage
- Advanced AI analysis with emotion detection
- GitHub Actions automation

## Quick Start

### 🚀 Method 1: Web Interface (Recommended)
```bash
# Windows
run.bat

# Linux/Mac
./deploy.sh

# Then open http://localhost:5000
```

### 🎬 Method 2: Command Line
```bash
python main.py --url "YOUR_YOUTUBE_URL"
```

## 🧪 Testing After GitHub Upload

### Automated Testing (GitHub Actions)
1. Go to your GitHub repository
2. Click "Actions" tab
3. Run "Test YouTube Shorts Generator" workflow
4. Enter YouTube URL and run

### Local Testing
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/clip_yt_ai.git
cd clip_yt_ai

# Install dependencies
pip install -r requirements.txt

# Run comprehensive test
python github_test.py

# Test web app
python web_app.py
```

### GitHub Codespaces Testing
1. Click "Code" → "Codespaces"
2. Create codespace
3. Run `python github_test.py`

## Installation
```bash
pip install -r requirements.txt
```

## Free APIs Used
- OpenAI Whisper (for transcription)
- Hugging Face Transformers (for content analysis)
- YouTube-dl (for video download)

## Documentation
- [Complete Usage Guide](USAGE_GUIDE.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Test Commands](TEST_COMMANDS.md)
