# YouTube Shorts Generator Deployment Script for Windows

Write-Host "🚀 Deploying YouTube Shorts Generator..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip is not installed. Please install pip first." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "generated_shorts" | Out-Null
New-Item -ItemType Directory -Force -Path "temp_files" | Out-Null
New-Item -ItemType Directory -Force -Path "templates" | Out-Null

# Run tests
Write-Host "🧪 Running tests..." -ForegroundColor Yellow
python test.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Tests failed!" -ForegroundColor Red
    exit 1
}

# Start web application
Write-Host "🌐 Starting web application..." -ForegroundColor Green
Write-Host "Open your browser and go to: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

python web_app.py
