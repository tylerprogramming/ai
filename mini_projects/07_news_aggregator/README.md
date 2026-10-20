# 07 News Aggregator

Four agents run one after another to build a weekly AI news roundup: `newsapibot` pulls articles from newsapi.org, `serperbot` searches Google News through serper.dev, `news_aggregator` summarizes both into a blog post of key points, and `file_writer` saves it to `news.md`.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put `OPENAI_API_KEY`, `NEWSAPI_API_KEY` and `SERPER_API_KEY` in a `.env` file, then:

```bash
python main.py
```
