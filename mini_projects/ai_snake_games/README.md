# Ai Snake Games

Asks a model to write the game Snake in Python. An `Assistant` agent writes the code, an executor agent saves and runs it in `code/`, and you get a turn after each round to give feedback (type `exit` to stop). The other `.py` files here are the games different models produced (Llama 3, Mistral, Phi-3, Gemma, GPT-4, ...).

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

`main.py` talks to a local model through [Ollama](https://ollama.com) (`ollama pull llama3`, then make sure Ollama is running on `localhost:11434`). Change `model=` to the model you pulled, or switch to the commented-out OpenAI client and put `OPENAI_API_KEY` in your environment. Then:

```bash
python main.py
```
