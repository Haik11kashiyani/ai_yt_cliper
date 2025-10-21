@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting YouTube Shorts Generator Web App...
echo Open your browser and go to: http://localhost:5000
echo.

python web_app.py

pause
