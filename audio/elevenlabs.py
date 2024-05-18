from elevenlabs.client import ElevenLabs
from elevenlabs import generate,play
import hashlib
from datetime import datetime
from config import AUDIO_OUTPUT

client = ElevenLabs() # (API key defaults to os.getenv(ELEVEN_API_KEY))
def generate_audio(input_text: str, input_voice: str='Rachel',file_label: str='audio'):

    audio=generate(text=input_text,voice='Rachel',model="eleven_multilingual_v2")
    #play(audio)
    # Generate filename and path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    input_hash = hashlib.md5(input_text.encode()).hexdigest()[:8]  # Short hash of input
    filename = f"{file_label}_{input_hash}_{timestamp}.mp3"
    filepath = AUDIO_OUTPUT / f"{filename}" # Could add folders by date: {datetime.now().date()}/

    # Save the audio file to the filepath
    with open(filepath, "wb") as file:
        file.write(audio)
    
    # Store metadata in database (pseudo-code)
    # db.insert({"filename": filename, "filepath": filepath, "user_id": user_id, "created_at": timestamp})
    print('done')
    return filename  # or return an ID/reference from the database
#audio=generate_audio('a')