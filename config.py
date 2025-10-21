# Configuration for YouTube Shorts Generator

# Video Settings
VIDEO_HEIGHT = 1920  # Shorts height
VIDEO_WIDTH = 1080   # Shorts width
MAX_SHORTS = 5       # Maximum number of shorts to generate

# Audio Settings
BACKGROUND_MUSIC_VOLUME = 0.05  # 5% volume for background music
AUDIO_FADE_DURATION = 0.5       # Fade in/out duration

# Text Settings
TEXT_FONT_SIZE = 50
TEXT_COLOR = 'white'
TEXT_FONT = 'Arial-Bold'
MAX_CHARS_PER_LINE = 30

# Processing Settings
BUFFER_TIME = 2      # Seconds to add before/after key moments
MIN_SIMILARITY = 0.3 # Minimum similarity for text matching

# Viral Keywords (Hindi + English)
VIRAL_KEYWORDS = [
    "amazing", "incredible", "unbelievable", "shocking", "wow", "omg",
    "you won't believe", "this will blow your mind", "wait for it",
    "अद्भुत", "अविश्वसनीय", "चौंकाने वाला", "वाह", "क्या बात है",
    "जबरदस्त", "शानदार", "बेहतरीन", "अच्छा", "बहुत अच्छा"
]

# Output Settings
OUTPUT_DIR = "generated_shorts"
TEMP_DIR = "temp_files"
