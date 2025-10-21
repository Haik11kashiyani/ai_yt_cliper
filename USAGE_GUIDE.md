# 🎬 YouTube Shorts Generator - Complete Usage Guide

## 📋 Overview
यह system YouTube के लॉन्ग फॉर्म वीडियो से automatically वायरल शॉर्ट्स बनाता है। यह AI-powered analysis, emotion detection, और advanced video editing का use करता है।

## 🚀 Quick Start

### Method 1: Web Interface (Recommended)
```bash
# Windows
run.bat

# Linux/Mac
./deploy.sh

# PowerShell
./deploy.ps1
```

फिर browser में जाकर `http://localhost:5000` open करें।

### Method 2: Command Line
```bash
python main.py --url "YOUR_YOUTUBE_URL"
```

## 🎯 Features

### ✅ Basic Features
- **YouTube Video Download**: किसी भी YouTube video को download करता है
- **AI Transcription**: Whisper AI का use करके accurate transcription
- **Content Analysis**: Viral moments identify करता है
- **Auto Cropping**: 9:16 aspect ratio में convert करता है
- **Background Music**: 5-6% volume में background music add करता है
- **Text Overlay**: Hindi/English text overlay
- **Multiple Person Detection**: Side-by-side layout for multiple people

### 🧠 Advanced Features
- **Emotion Detection**: Text का emotion analysis
- **Sentiment Analysis**: Positive/Negative sentiment detection
- **Audio Analysis**: Energy peaks और tempo analysis
- **Visual Interest Detection**: Motion और face detection
- **Viral Score Calculation**: Multiple factors के basis पर viral score
- **Dynamic Music**: Tempo के basis पर background music
- **Animated Text**: Smooth text animations

## 📁 Project Structure
```
clip_yt_ai/
├── main.py                 # Main generator script
├── advanced_generator.py    # Advanced AI features
├── web_app.py              # Flask web interface
├── config.py               # Configuration settings
├── test.py                 # Test script
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Web interface template
├── .github/workflows/
│   └── ci.yml             # GitHub Actions workflow
├── deploy.sh              # Linux/Mac deployment
├── deploy.ps1             # Windows PowerShell deployment
├── run.bat                # Windows batch file
└── README.md              # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.9+
- pip
- FFmpeg (for video processing)

### Install FFmpeg
```bash
# Windows (using chocolatey)
choco install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS (using homebrew)
brew install ffmpeg
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Usage Examples

### Example 1: Basic Usage
```python
from main import YouTubeShortsGenerator

generator = YouTubeShortsGenerator()
shorts = generator.generate_shorts("https://www.youtube.com/watch?v=VIDEO_ID")
```

### Example 2: Advanced Usage
```python
from main import YouTubeShortsGenerator

# Use advanced features
generator = YouTubeShortsGenerator(use_advanced=True)
shorts = generator.generate_shorts("https://www.youtube.com/watch?v=VIDEO_ID")

# Access advanced data
for short in shorts:
    print(f"Viral Score: {short['viral_score']}")
    print(f"Sentiment: {short['sentiment']}")
    print(f"Emotion: {short['emotion']}")
```

### Example 3: Web Interface
1. Run `python web_app.py`
2. Open `http://localhost:5000`
3. Paste YouTube URL
4. Click "शॉर्ट्स जेनरेट करें"
5. Wait for processing
6. Download generated shorts

## ⚙️ Configuration

`config.py` file में settings modify कर सकते हैं:

```python
# Video Settings
VIDEO_HEIGHT = 1920  # Shorts height
VIDEO_WIDTH = 1080   # Shorts width
MAX_SHORTS = 5       # Maximum shorts to generate

# Audio Settings
BACKGROUND_MUSIC_VOLUME = 0.05  # 5% volume

# Text Settings
TEXT_FONT_SIZE = 50
MAX_CHARS_PER_LINE = 30
```

## 🧪 Testing

```bash
# Run all tests
python test.py

# Test specific functionality
python -c "from main import YouTubeShortsGenerator; print('Import successful')"
```

## 🚀 Deployment

### Local Deployment
```bash
# Windows
run.bat

# Linux/Mac
./deploy.sh
```

### GitHub Actions
1. Push code to GitHub
2. Go to Actions tab
3. Run "YouTube Shorts Generator CI/CD" workflow
4. Provide YouTube URL in workflow_dispatch

### Cloud Deployment
```bash
# Heroku
git push heroku main

# Railway
railway deploy

# Render
Connect GitHub repository
```

## 🔍 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Install FFmpeg
   sudo apt install ffmpeg  # Linux
   brew install ffmpeg      # macOS
   choco install ffmpeg     # Windows
   ```

2. **Memory issues**
   ```python
   # Reduce video quality in main.py
   ydl_opts = {
       'format': 'worst[height<=480]',  # Lower quality
   }
   ```

3. **Model download issues**
   ```bash
   # Clear cache
   rm -rf ~/.cache/whisper
   rm -rf ~/.cache/huggingface
   ```

4. **Permission errors**
   ```bash
   # Linux/Mac
   chmod +x *.py
   chmod +x *.sh
   ```

## 📊 Output

Generated shorts में ये information होती है:
- **Text**: Original transcribed text
- **Duration**: Short duration in seconds
- **Face Count**: Number of faces detected
- **Viral Score**: AI-calculated viral potential
- **Sentiment**: Positive/Negative/Neutral
- **Emotion**: Joy/Surprise/Anger/Fear/etc.

## 🎨 Customization

### Custom Viral Keywords
`config.py` में अपने keywords add करें:
```python
VIRAL_KEYWORDS = [
    "amazing", "incredible", "your_keyword",
    "अद्भुत", "अविश्वसनीय", "आपका_कीवर्ड"
]
```

### Custom Text Styling
`main.py` में text styling modify करें:
```python
txt_clip = TextClip(line, fontsize=60, color='yellow', font='Arial-Bold')
```

### Custom Music
`advanced_generator.py` में music generation modify करें।

## 📈 Performance Tips

1. **Use SSD**: Faster video processing
2. **Increase RAM**: Better for large videos
3. **GPU Support**: Install CUDA for faster AI processing
4. **Batch Processing**: Process multiple videos together

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

## 📄 License

This project is open source. Feel free to use and modify.

## 🆘 Support

अगर कोई problem हो तो:
1. Check troubleshooting section
2. Run test script
3. Check logs for errors
4. Create GitHub issue

---

**Happy Shorts Generation! 🎬✨**
