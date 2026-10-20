# Reddit

A Streamlit app backed by an AutoGen "Engineer" agent with Reddit tools (via PRAW). Pick a random subreddit or name one, choose how many posts, and the agent fetches them and returns the posts' metadata and content as JSON for the app to display.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Create a Reddit "script" app at https://www.reddit.com/prefs/apps, then add a `.env` file (in this folder or the parent `_legacy_integrations` folder):

```
OPENAI_API_KEY=your-openai-key
CLIENT_ID=your-reddit-app-client-id
CLIENT_SECRET=your-reddit-app-client-secret
```

Then run:

```bash
streamlit run main.py
```

Note: PRAW 8 removed `random_subreddit()` (Reddit retired r/random), so "Random" mode now picks a random subreddit from the current popular list.
