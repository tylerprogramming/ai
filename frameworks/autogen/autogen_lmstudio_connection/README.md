# Autogen Lmstudio Connection

Connects an AutoGen assistant to a local model served by [LM Studio](https://lmstudio.ai/). The assistant writes a Magic 8 Ball function and a code-executor agent runs it locally in the `coding` folder.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

1. In LM Studio, load a model (the example uses `phi`) and start the local server on `http://localhost:1234`.
2. Install and run:

```bash
pip install -r requirements.txt
python main.py
```

No OpenAI key is needed: LM Studio exposes an OpenAI-compatible API, so the example points `OpenAIChatCompletionClient` at `base_url="http://localhost:1234/v1"`. Change `model=` in `main.py` to match the model you loaded.

> Code the model writes is executed on your machine without a sandbox. Read it before you let it run on anything important.
