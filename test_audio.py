from google import genai
from config import GEMINI_API_KEYS
import json

client = genai.Client(api_key=GEMINI_API_KEYS[0])

audio_path = "uploads/887c6cd2c3f548b4be09ad737a67694b_translated_fr_3.mp3"

uploaded_file = client.files.upload(
    file=audio_path
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        uploaded_file,
        """
        Transcribe this audio.

        Return ONLY JSON.

        {
          "detected_language":"",
          "transcript":""
        }
        """
    ]
)

print(response.text)