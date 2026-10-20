# 06 Meal Gym Planner

A Flask app that walks you through four short forms (profile, workout preferences, schedule, focus areas), then has AutoGen agents build a personalized workout plan and meal plan, combine them into JSON for the results page, and save a markdown copy to `workout_plan.md` for download.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in a `.env` file, then:

```bash
python app.py                  # http://localhost:5000
FLASK_DEBUG=1 python app.py    # with Flask debug mode
python workout_agents.py       # run the agents from the command line with a sample profile
```
