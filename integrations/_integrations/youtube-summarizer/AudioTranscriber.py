import io
import time
from pydub import AudioSegment
import openai


class AudioTranscriber:
    def __init__(self, api_key, model='whisper-1', chunk_duration=20):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.chunk_duration_ms = chunk_duration * 60 * 1000

    def transcribe_audio(self, filename):
        audio = AudioSegment.from_file(filename)
        transcription = ""
        for split_number, i in enumerate(range(0, len(audio), self.chunk_duration_ms)):
            chunk = audio[i: i + self.chunk_duration_ms]
            file_obj = io.BytesIO(chunk.export(format="mp3").read())
            file_obj.name = f"part_{split_number}.mp3"
            transcription += self.transcribe_chunk(file_obj, split_number)
        return transcription

    def transcribe_chunk(self, file_obj, split_number):
        print(f"Transcribing part {split_number + 1}!")
        attempts = 0
        while attempts < 3:
            try:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model, file=file_obj
                )
                return transcript.text
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts} failed. Exception: {str(e)}")
                time.sleep(5)
        print("Failed to transcribe after 3 attempts.")
        return ""
