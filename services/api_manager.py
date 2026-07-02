import os
from dotenv import load_dotenv

load_dotenv()

class APIKeyManager:

    def __init__(self, keys):
        self.keys = [k for k in keys if k]
        self.current = 0

    def get_key(self):
        if not self.keys:
            raise Exception("No API keys found.")
        return self.keys[self.current]

    def switch_key(self):
        if len(self.keys) > 1:
            self.current = (self.current + 1) % len(self.keys)
            print(f"Switched to API Key {self.current + 1}")


openai_manager = APIKeyManager([
    os.getenv("OPENAI_API_KEY_1"),
    os.getenv("OPENAI_API_KEY_2"),
])

gemini_manager = APIKeyManager([
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
])

elevenlabs_manager = APIKeyManager([
    os.getenv("ELEVENLABS_API_KEY_1"),
    os.getenv("ELEVENLABS_API_KEY_2"),
])