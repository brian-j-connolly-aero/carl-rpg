from elevenlabs.client import ElevenLabs
from elevenlabs import generate,play
client = ElevenLabs() # (API key defaults to os.getenv(ELEVEN_API_KEY))
def generate_audio(input_text: str):
    audio=generate(text="test test goes here!",voice='Rachel',model="eleven_multilingual_v2")
    play(audio)