# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:31:20 2024

Can't run in Spyder, must be cmd
Invite bot to server, join voice channel, run !start command to start, !stop to stop
Currently have transcription file path hardcoded, should be dynamic
No timestamps or anything, transcription is just text.
Transcription does grab Discord username! Seems to work alright with at least 2 people.
0.25s dead time when restarting recording, increase if there are errors

"""

from enum import Enum
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Converter, Context
import asyncio
from openai import OpenAI
import tempfile
from datetime import datetime
import re

import time
client = OpenAI()

transcription_file_name=f"transcriptions.txt"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable the members intent

bot = commands.Bot(command_prefix='!', intents=intents, debug_guilds=['1092651946856419379'])
connections = {}


# class Sinks(Enum):
#     mp3 = discord.sinks.MP3Sink()
#     wav = discord.sinks.WaveSink()
#     pcm = discord.sinks.PCMSink()
#     ogg = discord.sinks.OGGSink()
#     mka = discord.sinks.MKASink()
#     mkv = discord.sinks.MKVSink()
#     mp4 = discord.sinks.MP4Sink()
#     m4a = discord.sinks.M4ASink()


# class SinkConverter(Converter):
#     async def convert(self, ctx: Context, argument: str) -> discord.sinks.Sink:
#         try:
#             return Sinks[argument].value
#         except KeyError:
#             raise commands.BadArgument(f"'{argument}' is not a valid sink type.")


# async def save_temp_file(audio_chunk, user_id):
#     temp_file = tempfile.NamedTemporaryFile(delete=False)
#     with open(temp_file.name, 'wb') as file:
#         file.write(audio_chunk)
#     return temp_file.name

        
async def parse_and_sort_transcripts_v5(transcripts, id_list):
    merged_transcripts = []
    for transcript, user_id in zip(transcripts, id_list):
        # Normalize newlines and split the transcript into lines
        lines = transcript.replace('\r\n', '\n').strip().split('\n')
        i = 0
        while i < len(lines):
            # Find lines with timestamps
            if '-->' in lines[i]:
                timestamp = lines[i]
                i += 1
                text_lines = []
                # Collect all subsequent lines until an empty line or a new timestamp
                while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                text = ' '.join(text_lines).strip()
                # Convert the timestamp to a datetime object for sorting
                start_time = datetime.strptime(timestamp.split(' --> ')[0].strip(), '%H:%M:%S,%f')
                merged_transcripts.append((start_time, user_id, text))
            else:
                i += 1

    # Sort the merged transcripts by timestamp
    merged_transcripts.sort(key=lambda x: x[0])

    # Format the sorted transcripts
    formatted_transcript = "\n".join([f"{user_id}: {text}" for _, user_id, text in merged_transcripts])
    return formatted_transcript

async def finished_callback(sink, channel: discord.TextChannel, *args):
    
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    #await sink.vc.disconnect()
    await asyncio.sleep(2)
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]

    # Process each audio file
    transcripts=[]
    id_list=[]
    for user_id, audio in sink.audio_data.items():
        # Write BytesIO to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{sink.encoding}") as temp_file:
            temp_file_name = temp_file.name
            temp_file.write(audio.file.read())
        
        # Ensure the pointer is at the start
        audio.file.seek(0)
        
        # Transcribe the audio from the temporary file
        transcript = await transcribe_audio(client, temp_file_name, user_id)
        member = channel.guild.get_member(int(user_id))
        if member:
            user_name = member.display_name  # or member.name for the actual username
            id_list.append(user_name)
        else:
            id_list.append(user_id)
        
            
        transcripts.append(transcript)
        
        # Delete the temporary file after using it
        os.remove(temp_file_name)
    merged_transcripts = []
    for transcript, user_id in zip(transcripts, id_list):
        # Normalize newlines and split the transcript into lines
        lines = transcript.replace('\r\n', '\n').strip().split('\n')
        i = 0
        while i < len(lines):
            # Find lines with timestamps
            if '-->' in lines[i]:
                timestamp = lines[i]
                i += 1
                text_lines = []
                # Collect all subsequent lines until an empty line or a new timestamp
                while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                text = ' '.join(text_lines).strip()
                # Convert the timestamp to a datetime object for sorting
                start_time = datetime.strptime(timestamp.split(' --> ')[0].strip(), '%H:%M:%S,%f')
                merged_transcripts.append((start_time, user_id, text))
            else:
                i += 1

    # Sort the merged transcripts by timestamp
    merged_transcripts.sort(key=lambda x: x[0])

    # Format the sorted transcripts
    formatted_transcript = "\n".join([f"{user_id}: {text}" for _, user_id, text in merged_transcripts])
    
    await write_transcription_to_file("1", formatted_transcript)
    # Removing the voice connection from the connections dictionary
    #if sink.vc.guild.id in connections:
    #    del connections[sink.vc.guild.id]

async def transcribe_audio(client, audio_path, user_id):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="srt"
            )
        transcription_text=transcript
        # Call the function to write the transcription to a file
        #await write_transcription_to_file(user_id, transcription_text)
    except:
        transcription_text=""    
    return transcription_text

import os

TRANSCRIPTIONS_DIR = 'transcriptions'  # Directory to save transcription files

async def write_transcription_to_file(user_id, transcription, transcription_file_name):
    
    # Ensure the directory exists
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)
    
    # Define the file path
    file_path = os.path.join(TRANSCRIPTIONS_DIR, transcription_file_name)
    
    # Open the file and append the transcription
    with open(file_path, 'a') as file:
        file.write(transcription + "\n")



@bot.command()
async def start(ctx: commands.Context):  # Use commands.Context for type hinting
    """Record your voice in MP3 format!"""
    voice = ctx.author.voice

    if not voice:
        return await ctx.send("You're not in a voice channel right now.")  # Use ctx.send

    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})
    
    # Variable to control the recording loop
    is_recording = True
    
    await ctx.send("The recording has started!")
    while is_recording:
        if ctx.guild.id not in connections:
            break  # Stop if the bot is not connected to the channel anymore
            
        # Use the MP3 sink directly
        wav_sink = discord.sinks.WaveSink()#Sinks.mp3.value
        
        # Start recording
        vc.start_recording(
            wav_sink,
            finished_callback,
            ctx.channel,
        )
        
        # Wait for 20 seconds
        await asyncio.sleep(10)

        # Stop recording
        if ctx.guild.id in connections:
            vc.stop_recording()

            # (Optional) Short delay to ensure the recording is properly stopped before starting again
            await asyncio.sleep(.25)
        #del(mp3_sink)
    await ctx.send("Recording session ended.")

@bot.command()
async def stop(ctx: discord.ApplicationContext):
    """Stop recording and exit the recording loop."""
    global is_recording  # Make is_recording global to access it in this command
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.message.delete()
        await ctx.send("The recording has stopped!")
        is_recording = False  # Update the variable to stop the loop
    else:
        await ctx.send("Not recording in this guild.")





bot.run()
