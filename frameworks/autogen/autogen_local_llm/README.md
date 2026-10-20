# Autogen Local Llm

Runs an AutoGen assistant on a HuggingFace model loaded locally with `transformers` (default: `stabilityai/stable-code-3b` on CPU), through a small custom model client. The assistant writes a Hello World script and a code-executor agent runs it in the `coding` folder.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). A custom model is now a subclass of `ChatCompletionClient` (see `CustomModelClient.py`) passed straight to the agent — no JSON model config file or `register_model_client` needed.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

No API key is needed. The first run downloads the model from HuggingFace (a few GB). Change the model, device (`"cuda"`, `"mps"`) or `max_length` where `CustomModelClient(...)` is created in `main.py`.

> Code the model writes is executed on your machine without a sandbox. Read it before you let it run on anything important.
