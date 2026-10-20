# AutoGen Studio (YouTube Short)

Code from the AutoGen Studio short: `my-app/` is the Studio app folder from the recording (its `autogen.db` holds the teams and chat sessions), and `tictactoe.py` is the console Tic-Tac-Toe game the agents wrote.

## Run it

```bash
pip install -r requirements.txt
python tictactoe.py                         # play the generated game in the terminal
autogenstudio ui --appdir my-app --port 8081 # open http://127.0.0.1:8081
```

Put your `OPENAI_API_KEY` in your environment (or in Studio's settings) to run agents.

> **Note:** The short used an early AutoGen Studio 0.4 release. Current AutoGen Studio (0.4.2.x) keeps its data in a new versioned database (`autogen04202.db`) and regenerates `my-app/alembic/` on startup, so the original sessions in `autogen.db` don't show up in the new UI. `autogen.db` is kept as the original sample data. Starting Studio also rewrites the committed `my-app/alembic*` files, so expect `git status` to show changes after a run (`git checkout my-app` restores them).
