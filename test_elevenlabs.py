from services.elevenlabs_service import ElevenLabsService

service = ElevenLabsService()

voices = service.client.voices.get_all()

print(voices)