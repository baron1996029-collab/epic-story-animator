# Configuration for Epic Story Animator

# Ollama Configuration
OLLAMA_MODEL = "llama2"  # Change to "mistral" or another model if needed
OLLAMA_HOST = "http://localhost:11434"

# Video Configuration
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30
MAX_VIDEO_DURATION = 120  # 2 minutes in seconds

# Manim Configuration
MANIM_QUALITY = "high_quality"  # Options: low_quality, medium_quality, high_quality
MANIM_FRAME_RATE = 30

# Scene Configuration
MAX_SCENES = 5
SCENE_DURATION = 20  # seconds per scene

# Colors for animations
PRIMARY_COLOR = "#FFD700"  # Gold
SECONDARY_COLOR = "#DC143C"  # Crimson
ACCENT_COLOR = "#1E90FF"  # Dodger Blue
BACKGROUND_COLOR = "#0B0014"  # Dark purple

# Output Configuration
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
