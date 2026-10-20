# Autogen Human Interaction

An assistant writes three small Python functions and saves them to `tested_code/`, an executor runs the code, and you (the human) give feedback after every round. At the end the LLM summarizes the conversation and the full chat is saved to `conversations.json`. A commented-out block in `main.py` shows how to point it at a local LM Studio model instead.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```

Type feedback when prompted, or `exit` to end the chat.
