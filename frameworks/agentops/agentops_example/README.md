# Agentops Example

An AutoGen group chat (planner, engineer, critic and a code executor) that plans and builds a small Bootstrap front end, with the whole run recorded in [AgentOps](https://www.agentops.ai/) so you can replay the agents' messages, LLM calls and costs in the AgentOps dashboard.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your keys in a `.env` file:

```
OPENAI_API_KEY=...
AGENTOPS_API_KEY=...
```

Then run:

```bash
python groupchat.py
```

When the agents finish you can type feedback to keep going, or `exit` to end the session.
