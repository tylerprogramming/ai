# Autogen Logging

Logs an AutoGen run and inspects it afterwards: an assistant answers one question while every LLM call is written to `logs.jsonl`, then the script prints token usage and a pandas table of the logged requests and responses.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). The 0.2 sqlite runtime logger (`autogen.runtime_logging`) is gone; v0.7 emits structured events (including each LLM call) to the standard Python logger named `autogen_core.EVENT_LOGGER_NAME`, which this example writes to a JSON-lines file.

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```
