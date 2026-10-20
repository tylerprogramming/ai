# OpenAI Swarm examples

Small examples for [OpenAI Swarm](https://github.com/openai/swarm), OpenAI's experimental multi-agent framework.

> **Swarm is archived.** OpenAI replaced it with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (see `../openai_sdk/`). These examples still install and run, but Swarm gets no updates. Its `instructor` dependency holds `openai` at 3.3.x, so use a separate virtualenv for this folder.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Examples

| Run | What it shows |
|---|---|
| `python main.py` | Agent A hands off to Agent B (who only speaks in haikus), streamed. |
| `cd weather_agent && python run.py` | A REPL with a weather agent that has `get_weather` and `send_email` tools. |
| `cd personal_shopper && python run.py` | A triage agent that transfers to a sales or refunds agent. Uses the SQLite `application.db` in that folder. |

The REPL examples run until you press Ctrl-C.

> **Note:** Updated for current models (`gpt-5.4-mini`), and the personal shopper agents now use Swarm's `instructions`/transfer functions; the code may differ slightly from the video.
