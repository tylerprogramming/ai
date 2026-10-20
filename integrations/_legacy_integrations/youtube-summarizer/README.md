# Youtube Summarizer

Downloads the audio of a YouTube video with yt-dlp, transcribes it with OpenAI Whisper, then an AutoGen agent summarizes it (title + bullet points) and a second agent translates the summary into Dutch.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

Install [FFmpeg](https://ffmpeg.org/) first (needed for audio extraction), then:

```bash
pip install -r requirements.txt
```

Put your key in a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
```

Set the video `url` in `main.py`, then run:

```bash
python main.py
```

The audio file (`.m4a`) is saved in the folder you run it from.
