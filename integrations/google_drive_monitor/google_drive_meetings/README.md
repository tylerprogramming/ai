# Google Drive Monitor + CrewAI

Watches a Google Drive folder ("company files") for new files. Each new file is downloaded to `downloads/`, then a CrewAI Flow decides what kind of file it is:

- **Meeting recording (.wav)** → transcribed with OpenAI `gpt-transcribe` in 1-minute chunks → meeting-minutes crew (summary, action items, sentiment, written minutes)
- **Anything else (e.g. a contract PDF)** → parsed with LlamaParse → contract-management crew (key terms report)

The result is saved to Airtable and a notification is sent to Telegram.

> **Note:** Updated for CrewAI 1.15 and the new `llama-cloud` SDK; the code may differ slightly from the video. The video uses `whisper-1`, which OpenAI removes from the API on February 26, 2027 ([deprecations](https://developers.openai.com/api/docs/deprecations)); the code now uses its recommended replacement, `gpt-transcribe` ($0.0045 per audio minute).

## Setup

1. Install [FFmpeg](https://ffmpeg.org/) (used to read the audio), then:

   ```bash
   pip install -r requirements.txt
   ```

2. In Google Cloud Console, enable the **Google Drive API**, create an **OAuth client ID** (Desktop app) and download it as `credentials.json` into this folder. On the first run a browser window asks you to sign in, and the login is saved to `token.json`. Both files are secrets and are git-ignored.

3. Create a `.env` file in this folder (see `googledrive/.env.example`):

   ```
   OPENAI_API_KEY=
   LLAMA_API_KEY=          # LlamaCloud API key (LlamaParse)
   AIRTABLE_API_KEY=
   AIRTABLE_BASE_ID=
   AIRTABLE_TABLE_NAME=    # table with columns file_name, final_summary, telegram_message
   TELEGRAM_BOT_TOKEN=
   TELEGRAM_CHAT_ID=
   ```

## Run it

From this folder:

```bash
python drive_monitor.py
```

Change `FOLDER_NAME` in `drive_monitor.py` to watch a different Drive folder. Sample files to upload are in `downloads/`.
