# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 18:58:54 2024

@author: cavsf
"""

from openai import OpenAI
client = OpenAI()

audio_file = open("cheevo_ai7.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text"
)
print(transcript)