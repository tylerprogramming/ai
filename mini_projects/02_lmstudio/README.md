# **Repository** - Direct connection to LM Studio with OpenAI API
### This will help you if you want just a direct connection to LM Studio for an AI Agent.

LM Studio's local server speaks the OpenAI API, so the plain `openai` client works against it.

## Run

1. In LM Studio, load a model and start the local server (default `http://localhost:1234`).
2. Install and run:

```bash
pip install -r requirements.txt
python example_01.py   # one-shot completion
python example_02.py   # streaming chat loop (Ctrl-C to quit)
python example_03.py   # asks for a word, returns 3 rhymes
```

No API key is needed; the scripts pass `api_key="not-needed"`.

## Library Versions:
- Originally recorded with openai 1.6.1 and LM Studio 0.2.10; verified with openai 3.35.
