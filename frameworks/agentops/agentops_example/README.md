# Agentops Example

An AutoGen group chat (planner, engineer, critic and a code executor) that plans and builds a small Bootstrap front end, with the whole run recorded in [AgentOps](https://www.agentops.ai/) so you can see the LLM calls, token usage and costs in the AgentOps dashboard. (AgentOps 0.4 records the OpenAI calls; it doesn't yet trace AutoGen v0.7 agent messages the way it did for 0.2.)

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
