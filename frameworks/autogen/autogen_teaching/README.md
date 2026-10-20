# Autogen Teaching

A teachable agent: tell it facts about yourself (your favorite language, hobbies, birthday) and it saves them to a persistent ChromaDB memory, so it still remembers them the next time you run the script.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). v0.7 has no `Teachability` capability, so the idea is rebuilt with a persistent `ChromaDBVectorMemory` plus a `remember` tool the agent calls to save what you teach it.

## Run it

```bash
pip install -r requirements.txt
# put OPENAI_API_KEY in .env
python teachable_agents.py
```

You reply to the agent after each message; type `exit` to end the chat. Switch the task in `main()` to `task` to teach it about you, then to `task_check` to see that it remembers your birthday.

The memory is stored in `tmp/notebook/teachability_db`; delete that folder to reset it. ChromaDB's default embedding model is downloaded on the first run, so that run needs internet access.
