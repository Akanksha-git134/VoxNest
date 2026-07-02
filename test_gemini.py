from google import genai
from config import GEMINI_API_KEYS

client = genai.Client(
    api_key=GEMINI_API_KEYS[0]
)

print(client)
print(dir(client))