# Autogen Multiple Configs

Different ways to set up model connections for your agents: from a `.env` file, from key/base-URL text files, from lists of keys and URLs, and two assistants that each use their own model. Each script builds the model clients and prints their config (API keys are masked).

Updated to AutoGen v0.7 (the new `autogen_agentchat` API). v0.7 has no config lists (the JSON config file and its helper functions): you create one `OpenAIChatCompletionClient` per model and pass it to the agent as `model_client`.

## Run it

```bash
pip install -r requirements.txt
# put OPENAI_API_KEY in .env
python config_list_from_json.py      # or config_list_from_dotenv.py, config_list_openai_aoai.py, get_config_list.py
```

The files in `txt/` hold sample placeholder keys and URLs for `config_list_openai_aoai.py`; replace them with your own.
