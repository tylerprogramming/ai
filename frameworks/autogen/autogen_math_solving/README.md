# Autogen Math Solving

Solves a competition-style math problem with two agents: an assistant works through it step by step in Python, and a code-executor agent runs that code locally (in the `coding` folder) and returns the output until the assistant gives the final answer.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). AutoGen 0.2's `MathUserProxyAgent` (MathChat) doesn't exist in v0.7, so the same idea is rebuilt with an `AssistantAgent` + `CodeExecutorAgent` in a `RoundRobinGroupChat`.

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```

> Code the model writes is executed on your machine without a sandbox. Read it before you let it run on anything important.
