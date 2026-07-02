import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2")
]

ELEVENLABS_API_KEYS = [
    os.getenv("ELEVENLABS_API_KEY_1"),
    os.getenv("ELEVENLABS_API_KEY_2")
]