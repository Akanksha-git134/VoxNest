from google import genai
from config import GEMINI_API_KEYS
import json


class GeminiService:

    def __init__(self):

        self.current_key = 0

        self.client = genai.Client(
            api_key=GEMINI_API_KEYS[self.current_key]
        )

    def switch_api_key(self):

        if self.current_key + 1 >= len(GEMINI_API_KEYS):
            raise Exception("All Gemini API keys have exhausted their quota.")

        self.current_key += 1

        print(f"\n🔄 Switching to Gemini API Key #{self.current_key + 1}")

        self.client = genai.Client(
        api_key=GEMINI_API_KEYS[self.current_key]
        )

    def transcribe_audio(self, audio_path):

        uploaded_file = self.client.files.upload(
            file=audio_path
        )

        prompt = """
        Analyze this audio.

        Return ONLY valid JSON.

        {
            "detected_language":"",
            "transcript":""
        }
        """

        while True:

            try:

                response = self.client.models.        generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        uploaded_file,
                        prompt
                    ]
                )

                break

            except Exception as e:

                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):

                    self.switch_api_key()

                else:

                    raise e

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        try:
            return json.loads(text)

        except Exception:
            return {
                "detected_language": "Unknown",
                "transcript": text
            }

    def translate_text(self, transcript, target_language):

        prompt = f"""
        You are a professional translator.

        Translate the following text into {target_language}.

        Rules:
        - Only return the translated text.
        - Do not explain anything.
        - Preserve names and numbers.
        - Keep the meaning natural.

        Text:
        {transcript}
        """
        
        while True:

            try:

                response = self.client.models.        generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                break

            except Exception as e:

                if "429" in str(e) or         "RESOURCE_EXHAUSTED" in str(e):

                    self.switch_api_key()

                else:

                    raise e
        
        translated = response.text.strip()

        print("Gemini Translation:")
        print(translated)

        return translated