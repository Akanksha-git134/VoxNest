from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEYS

import os
import uuid

class ElevenLabsService:

    def __init__(self):

        self.client = ElevenLabs(
            api_key=ELEVENLABS_API_KEYS[0]
        )

    def text_to_speech(
        self,
        text,
        voice_id,
    ):

        audio = self.client.text_to_speech.convert(

            voice_id=voice_id,

            model_id="eleven_multilingual_v2",

            text=text,

            output_format="mp3_44100_128"
        )

        os.makedirs("static/audio", exist_ok=True)

        filename = f"translated_{uuid.uuid4().hex}.mp3"

        filepath = os.path.join(
            "static/audio",
            filename
        )

        with open(filepath, "wb") as f:

            for chunk in audio:

                if chunk:

                    f.write(chunk)

        return "/static/audio/" + filename
    
    def get_all_voices(self):

        return self.client.voices.get_all().voices