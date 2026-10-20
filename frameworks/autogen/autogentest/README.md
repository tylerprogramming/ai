# Autogentest

A few early AutoGen experiments:

- `topten.py` - an assistant writes and runs code to plot the top 10 countries by land mass (you can give feedback after each run; type `exit` to stop).
- `saas_customer_survey.py` - a Planner, Engineer, Executor and Critic build a small Flask + sqlite feedback website (output saved in `feedback/`).
- `llama_lm_test.py` - a content-creator team writing a YouTube script, running on a local LLM through LM Studio.

The `code/` and `feedback/` folders contain files the agents generated in earlier runs.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in a `.env` file, then:

```bash
python topten.py
python saas_customer_survey.py
```

For `llama_lm_test.py`, start the LM Studio local server on port 1234 first (no API key needed).
