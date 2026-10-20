# Autogen Memgpt Lmstudio

A group chat between a user (who runs the code), a product manager and a coder, powered by a local model in [LM Studio](https://lmstudio.ai/) or by OpenAI. Set `USE_MEMGPT = True` to swap the coder for an agent with its own memory: it can save facts with a `remember` tool, and AutoGen adds them to its context on every turn.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). MemGPT (`pymemgpt`) has been discontinued (it is now [Letta](https://www.letta.com/)), so the memory agent is rebuilt with AutoGen's built-in `ListMemory`.

## Run it

1. In LM Studio, load a model that supports tool calling and start the local server on `http://localhost:1234`.
2. Install and run:

```bash
pip install -r requirements.txt
python autogen_memgpt_lmstudio.py
```

To use OpenAI instead, put `LLM_BACKEND=openai` and `OPENAI_API_KEY` in a `.env` file.

> Code the agents write is executed on your machine (in the `groupchat` folder) without a sandbox.
