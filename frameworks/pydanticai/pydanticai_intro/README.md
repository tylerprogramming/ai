# PydanticAI intro

Two starter scripts for [PydanticAI](https://ai.pydantic.dev/).

| Script | What it does |
|---|---|
| `hello-world.py` | One-sentence answer from `openai:gpt-5.4-mini`. |
| `web-scraper.py` | An agent with a `scrape_website` tool (Firecrawl) that returns a typed `ScrapedContent` (summary + keypoints). Spans go to Logfire if you have a Logfire token configured. |

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
export FIRECRAWL_API_KEY=fc-...   # web-scraper.py only
python hello-world.py
python web-scraper.py
```

> **Note:** Updated for pydantic-ai 2.58 (`output_type` / `result.output`) and firecrawl-py 4.x (`Firecrawl().scrape`); the code may differ slightly from the video.
