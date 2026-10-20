# Autogen Agentbuilder

Builds a team of AI agents automatically: the LLM writes a profile for each job position (saved as an agent library in `agents.json`), a builder agent picks the best agents from that library for the task (saved to `autogen_ab`), and the chosen agents then work together in a group chat to write a Python function.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). v0.7 has no `AgentBuilder`, so `main.py` rebuilds the same steps with structured output and a `SelectorGroupChat`.

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```
