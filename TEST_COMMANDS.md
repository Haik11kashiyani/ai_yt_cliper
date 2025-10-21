# GitHub Repository Testing Commands

# 1. Clone the repository
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
# Then open http://localhost:5000 in browser

# 6. Test with sample video
python main.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 7. Check generated output
ls generated_shorts/
