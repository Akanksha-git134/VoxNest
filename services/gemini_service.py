from google import genai
from config import GEMINI_API_KEYS
import json
import time
import subprocess

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

    def transcribe_audio(self, path):

        import os

        print("Audio Path:", path)
        print("File Exists:", os.path.exists(path))
        print("File Size:", os.path.getsize(path))
        
        # ----------------------------------------
        # Convert recorded WEBM to WAV
        # ----------------------------------------

        import os
        import subprocess

        extension = os.path.splitext(path)[1].lower()

        if extension != ".wav":

            wav_path = os.path.splitext(path)[0] + ".wav"

            subprocess.run([
                "ffmpeg",
                "-y",
                "-i",
                path,
                wav_path
            ], check=True)

            print("Converted to:", wav_path)

            path = wav_path

        print("Converted to:", path)
        
        uploaded_file = self.client.files.upload(
            file=path
        )

        max_attempts = 15
        attempt = 0

        while attempt < max_attempts:

            file_info = self.client.files.get(
                name=uploaded_file.name
            )

            print(file_info)
            print("Gemini Status:", file_info.state)

            state = str(file_info.state)

            if state == "FileState.ACTIVE":
                break

            if state == "FileState.FAILED":
                raise Exception(
                    f"Gemini failed to process the uploaded audio.\n\nFile Info:\n{file_info}"
                )

            time.sleep(2)

            attempt += 1

        if attempt == max_attempts:
            raise Exception(
                "Gemini processing timed out."
            )

        prompt = """
        Analyze this audio carefully.

        The speaker may mix multiple languages in one sentence
        (for example Hindi + English, Tamil + English, etc.).

        Preserve names, numbers, abbreviations and English technical terms exactly.

        Return ONLY valid JSON.

        Rules:
        - detected_language MUST be the full English language name.
        - Never return language codes like "en", "hi", "fr", "de".
        - Examples:
          English
          Hindi
          Tamil
          French
          German
          Japanese

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

                    print("Quota exceeded. Switching API key...")

                    self.switch_api_key()

                    # Upload the file again using the NEW API key
                    uploaded_file = self.client.files.upload(
                        file=path
                    )

                    # Wait until Gemini finishes processing
                    while True:

                        file_info = self.client.files.get(
                            name=uploaded_file.name
                        )

                        print("New Upload Status:", file_info.state)

                        if str(file_info.state) == "FileState.ACTIVE":
                            break

                        time.sleep(2)

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

        Translate the following text into         {target_language}.

        Rules:
        - Preserve the original meaning exactly.
        - Keep the translation natural and fluent.
        - Be consistent in terminology.
        - Preserve names, numbers, brands, and technical terms.
        - Do not add or remove information.
        - Return ONLY the translated text.

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