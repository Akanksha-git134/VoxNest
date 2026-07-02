from google import genai
from config import GEMINI_API_KEYS

client = genai.Client(
    api_key=GEMINI_API_KEYS[0]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello."
)

print(response.text)