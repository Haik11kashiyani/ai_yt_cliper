#!/bin/bash

# YouTube Shorts Generator Deployment Script

echo "🚀 Deploying YouTube Shorts Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p generated_shorts
mkdir -p temp_files
mkdir -p templates

# Set permissions
echo "🔐 Setting permissions..."
chmod +x main.py
chmod +x web_app.py
chmod +x test.py

# Run tests
echo "🧪 Running tests..."
python3 test.py

if [ $? -eq 0 ]; then
    echo "✅ Tests passed!"
else
    echo "❌ Tests failed!"
    exit 1
fi

# Start web application
echo "🌐 Starting web application..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"

python3 web_app.py
