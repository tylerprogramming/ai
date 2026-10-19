# 00 Getting Started

Your first AutoGen agents: `first_agents.py` has an engineer agent write a small Python file that a code executor then runs, and `group_chat.py` puts a planner, engineer, critic and code executor in a group chat to plan a multi-page Bootstrap front end.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in a `.env` file, then:

```bash
python first_agents.py
python group_chat.py
```

Generated code is saved to `coding/` and `code/`. In `group_chat.py` you can give the agents feedback when they finish, or type `exit` to end.
