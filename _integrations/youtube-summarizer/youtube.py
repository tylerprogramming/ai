import yt_dlp
import os
import io
import time
from dotenv import load_dotenv
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
)
from pydub import AudioSegment

import openai

load_dotenv()

URLS = ['https://www.youtube.com/watch?v=LQRuaP2VFfA']

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Audio file from disk
audio = AudioSegment.from_file("./test.m4a")

# Define the duration of each chunk in minutes
# Need to meet 25MB size limit for Whisper API
chunk_duration = 20
chunk_duration_ms = chunk_duration * 60 * 1000

# Split the audio into chunk_duration_ms chunks
for split_number, i in enumerate(range(0, len(audio), chunk_duration_ms)):
    # Audio chunk
    chunk = audio[i: i + chunk_duration_ms]
    # Skip chunks that are too short to transcribe
    # if chunk.duration_seconds <= self.chunk_duration_threshold:
    #     continue
    file_obj = io.BytesIO(chunk.export(format="mp3").read())
    # if blob.source is not None:
    #     file_obj.name = blob.source + f"_part_{split_number}.mp3"
    # else:
    file_obj.name = f"part_{split_number}.mp3"

    # Transcribe
    print(f"Transcribing part {split_number + 1}!")  # noqa: T201
    attempts = 0
    while attempts < 3:
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=file_obj
            )
            break
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed. Exception: {str(e)}")  # noqa: T201
            time.sleep(5)
    else:
        print("Failed to transcribe after 3 attempts.")  # noqa: T201
        continue

    print(transcript.text)
