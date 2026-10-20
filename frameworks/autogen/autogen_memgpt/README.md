# Autogen Memgpt

A group chat between you (the human admin), a product manager and a coder that builds a small Flask app with a random-number button; a code-executor agent runs the code in the `groupchat` folder. Set `use_memgpt=1` to swap the coder for a version with long-term memory.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). MemGPT (`pymemgpt`) has been discontinued (it continues as [Letta](https://www.letta.com)), so the memory coder is rebuilt with AutoGen's built-in `ListMemory` plus a `remember` tool the agent uses to save facts.

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python app.py                 # regular coder
use_memgpt=1 python app.py    # coder with memory
```

When it's your turn, type a reply, or `exit` to end the chat.

> Code the model writes is executed on your machine without a sandbox. Read it before you let it run on anything important.
