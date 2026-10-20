# **Autogen + Integrations**
One thing I think is somewhat missing from Autogen is API Integration with other...well API's.  This is something Langchain does well.  But my goal is to add more than what they offer for some of these API's.

> **Note:** Updated to AutoGen v0.7 (the new `autogen_agentchat` API). Each project has its own `requirements.txt` (`pip install -r requirements.txt`) and README.

## Imports Needed:
### Airtable
- autogen-agentchat, autogen-ext[openai]
- pyairtable
### Reddit
- autogen-agentchat, autogen-ext[openai]
- praw (this stands for **Python Reddit API Wrapper**)
- streamlit
### Youtube Summarizer
- autogen-agentchat, autogen-ext[openai]
- openai, pydub, yt-dlp (plus FFmpeg)

## .env
- BASE_ID=airtable base id
- API_KEY=airtable api key (may re-name this in future)
- OPENAI_API_KEY=openai's api key
- CLIENT_ID=the id after creating reddit app
- CLIENT_SECRET=the secret after creating reddit app

## YouTube Link:
- coming soon

## Updates:
- 05/30/2024: Added Airtable Integration
- 06/02/2024: Added Reddit Integration
- 10/20/2026: Updated all projects to AutoGen v0.7

