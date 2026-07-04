from services.gemini_service import GeminiService
from services.elevenlabs_service import ElevenLabsService
import os

class TranslationPipeline:

    def __init__(self): 

        self.gemini = GeminiService()
        self.tts = ElevenLabsService()

    def process_audio(
        self,
        path,
        target_language,
        voice_id,
    ):


        wav_path = os.path.splitext(path)[0] + ".wav"

        try:

            transcript_data = (
                self.gemini.transcribe_audio(path)
            )
            
            detected = transcript_data["detected_language"].strip().title()

            target = target_language.strip().lower()

            if detected.lower() == target:
                return {
                "success": False,
                "error": "Source and target languages are         the same. Please choose another language."
            }

            print("Transcript:", transcript_data["transcript"])
            print("Translate To:", target_language)

            translated_text = (
                self.gemini.translate_text(
                    transcript_data["transcript"],
                    target_language
                )
            )

            voice_url = self.tts.text_to_speech(
                translated_text,
                voice_id
            )

            return {

                "success": True,

                "detected_language":
                detected,

                "transcript":
                transcript_data["transcript"],

                "translated_text":
                translated_text,

                "voice_url":
                voice_url

            }

        finally:

            if os.path.exists(path):

                os.remove(path)

                print("Deleted:", path)

            if os.path.exists(wav_path):

                os.remove(wav_path)

                print("Deleted:", wav_path)
        
        