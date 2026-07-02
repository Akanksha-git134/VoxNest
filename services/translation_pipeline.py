from services.gemini_service import GeminiService
from services.elevenlabs_service import ElevenLabsService

class TranslationPipeline:

    def __init__(self): 

        self.gemini = GeminiService()
        self.tts = ElevenLabsService()

    def process_audio(
        self,
        audio_path,
        target_language,
        voice_id,
    ):


        transcript_data = (
            self.gemini.transcribe_audio(audio_path)
        )
        
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
            transcript_data["detected_language"],

            "transcript":
            transcript_data["transcript"],
        
            "translated_text":
            translated_text,

            "voice_url":
            voice_url

}