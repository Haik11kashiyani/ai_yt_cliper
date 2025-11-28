import os

# 1. Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Define the missing VIDEO_DIR variable
VIDEO_DIR = os.path.join(BASE_DIR, "videos")

# 3. Define other useful paths
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_shorts")

# 4. Create directories if they don't exist
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 5. Settings
MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 60
