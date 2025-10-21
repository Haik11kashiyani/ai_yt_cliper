from flask import Flask, render_template, request, jsonify, send_file
import os
import threading
from main import YouTubeShortsGenerator
import json

app = Flask(__name__)

# Global variable to track generation status
generation_status = {
    "is_running": False,
    "progress": 0,
    "message": "",
    "shorts": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_shorts():
    global generation_status
    
    if generation_status["is_running"]:
        return jsonify({"error": "Generation already in progress"}), 400
    
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Start generation in background thread
    thread = threading.Thread(target=generate_shorts_background, args=(url,))
    thread.start()
    
    return jsonify({"message": "Generation started"})

def generate_shorts_background(url):
    global generation_status
    
    try:
        generation_status["is_running"] = True
        generation_status["progress"] = 0
        generation_status["message"] = "Starting generation..."
        generation_status["shorts"] = []
        
        generator = YouTubeShortsGenerator()
        
        # Update progress
        generation_status["progress"] = 10
        generation_status["message"] = "Downloading video..."
        
        # Download video
        video_path, video_info = generator.download_video(url)
        
        generation_status["progress"] = 30
        generation_status["message"] = "Extracting audio and transcribing..."
        
        # Extract audio and transcribe
        segments, full_text = generator.extract_audio_and_transcribe(video_path)
        
        generation_status["progress"] = 50
        generation_status["message"] = "Analyzing content..."
        
        # Analyze content
        viral_moments = generator.analyze_content(full_text)
        
        generation_status["progress"] = 70
        generation_status["message"] = "Finding timestamps..."
        
        # Find timestamps
        moments_with_timestamps = generator.find_timestamps_for_moments(viral_moments, segments)
        
        generation_status["progress"] = 80
        generation_status["message"] = "Generating shorts..."
        
        # Generate shorts
        output_dir = "generated_shorts"
        os.makedirs(output_dir, exist_ok=True)
        
        generated_shorts = []
        
        for i, moment in enumerate(moments_with_timestamps[:5]):
            start_time = max(0, moment["start"] - 2)
            end_time = min(video_info.get('duration', 3600), moment["end"] + 2)
            
            face_count = generator.detect_faces_and_people(video_path, start_time, end_time)
            
            output_path = f"{output_dir}/short_{i+1}.mp4"
            generator.create_short_video(video_path, start_time, end_time, output_path, moment["text"], face_count)
            
                short_data = {
                    "path": output_path,
                    "text": moment["text"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "face_count": face_count,
                    "filename": f"short_{i+1}.mp4"
                }
                
                # Add advanced data if available
                if hasattr(moment, 'viral_score'):
                    short_data["viral_score"] = moment["viral_score"]
                if hasattr(moment, 'sentiment'):
                    short_data["sentiment"] = moment["sentiment"]["label"]
                if hasattr(moment, 'emotion'):
                    short_data["emotion"] = moment["emotion"]["label"]
                
                generated_shorts.append(short_data)
        
        # Cleanup
        os.remove(video_path)
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        
        generation_status["progress"] = 100
        generation_status["message"] = "Generation completed!"
        generation_status["shorts"] = generated_shorts
        
    except Exception as e:
        generation_status["message"] = f"Error: {str(e)}"
        generation_status["progress"] = 0
    
    finally:
        generation_status["is_running"] = False

@app.route('/status')
def get_status():
    return jsonify(generation_status)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('generated_shorts', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
