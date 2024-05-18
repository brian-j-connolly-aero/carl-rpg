# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 19:53:54 2024

@author: cavsf
"""

from openai import OpenAI
from chorus import apply_chorus
import pyaudio
import numpy as np

# client = OpenAI()

# response = client.audio.speech.create(
#     model="tts-1",
#     voice="alloy",
#     input="""New Achievement!: Wax On, Face Down. <break time=".75s" />
# Fell over while back country skiing due to believing in the magic of 'no wax' ski treatment.
# Reward: You've received a bronze pity box.""",
# )

# response.stream_to_file("output.mp3")
def bytes_to_np_array(byte_data, sample_width, channels):
    dtype = np.int16 if sample_width == 2 else np.int8  # Assuming 16-bit or 8-bit samples
    audio_array = np.frombuffer(byte_data, dtype=dtype)
    if channels > 1:
        audio_array = audio_array.reshape((-1, channels))
    return audio_array

def np_array_to_bytes(audio_array):
    return audio_array.astype(np.int16).tobytes()




# Example usage
input_text = "Hello world! This is a streaming test."
#stream_and_process_audio(input_text)
client = OpenAI()

# Initialize PyAudio
p = pyaudio.PyAudio()
sample_rate=24000
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True)

response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    response_format="wav",
    input=input_text,
)

# Process the streaming audio
try:
    for chunk in response.iter_bytes():
        if chunk:
            # Convert bytes to numpy array
            audio_array = bytes_to_np_array(chunk, sample_width=2, channels=1)
            
            # Apply chorus effect
            processed_audio = apply_chorus(audio_array, sr=sample_rate)
            
            # Convert back to bytes
            processed_bytes = np_array_to_bytes(processed_audio)
            
            # Stream the processed audio
            stream.write(processed_bytes)
finally:
    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()