# Crawl4AI

Small examples for [Crawl4AI](https://github.com/unclecode/crawl4ai), an open-source web crawler/scraper that turns pages into LLM-friendly Markdown. No API keys needed.

| Script | What it does |
|--------|--------------|
| `01_first_crawl.py` | Crawls one page and prints its Markdown |
| `02_sequential.py` | Crawls a list of CrewAI docs pages one after another, reusing one browser |
| `03_quick_crawl.py` | Reads the CrewAI docs sitemap and crawls every URL in parallel batches |
| `crawl_crew/` | A CrewAI crew whose custom tool crawls a sitemap with Crawl4AI (see its own README) |

## Run

```bash
pip install -r requirements.txt
crawl4ai-setup          # one-time: installs the headless Chromium browser Crawl4AI uses
python 01_first_crawl.py
python 02_sequential.py
python 03_quick_crawl.py
```

Tested with Crawl4AI 0.9.5 (Python 3.10+).
