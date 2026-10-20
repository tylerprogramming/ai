# 03 Video Captions

A `chatbot` agent that takes a video file, transcribes it with Whisper and burns the captions into a new video with MoviePy. The transcribe-and-caption step is a tool (`functions.recognize_transcript_from_video`) the agent calls itself.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in a `.env` file (plus `base_dir`, the folder the captioned video is written under). FFMPEG is required for Whisper. Then call the agent from your own code:

```python
import asyncio
import agents

print(asyncio.run(agents.caption_video("Caption the video uploads/my_video.mp4 and name it my_video_captioned")))
```
