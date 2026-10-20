# Autogen Graphs

A research team with a fixed speaking order: the coder writes code to fetch recent LLM papers from the arXiv API, the executor runs it (sending errors back to the coder to fix), and the scientist sorts the papers into a markdown table (see `test.md` for a sample result). The order is controlled by a custom `selector_func` instead of letting the model pick the next speaker.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```
