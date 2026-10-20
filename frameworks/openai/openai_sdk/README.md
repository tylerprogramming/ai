# OpenAI Agents SDK: agents as tools

`handoff_openai.py` shows the agents-as-tools pattern with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`pip install openai-agents`, imported as `agents`). An orchestrator agent calls Spanish, French and Italian translator agents as tools, then a synthesizer agent combines their output.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python handoff_openai.py
```

Type a message and the languages you want, e.g. `Translate "good morning" to Spanish and Italian`.

> **Note:** Updated for openai-agents 0.24; the code may differ slightly from the video.
