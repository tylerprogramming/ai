# Autogen Transcribe Video

An agent that transcribes a video with OpenAI Whisper and translates the transcript into another language as subtitle text. It calls two tools: one that writes `transcription.txt` with timestamps, and one that translates it into `<language>_transcription.txt`.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

Whisper needs [FFmpeg](https://ffmpeg.org/) installed on your machine.

```bash
pip install -r requirements.txt
# put OPENAI_API_KEY in .env
python transcribe.py
```

The script asks for the video path, the source language and the target language.
