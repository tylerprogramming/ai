# OpenAI Agents API demo (video 058)

Three small scripts against the OpenAI Agents API (public beta, launched 2026-09-10). The API exposes the Codex harness as a managed service: OpenAI runs the agent loop, the sandbox, context compaction, and subagents. You send input and read events.

Each script is under 80 lines and meant to be read top to bottom on screen.

| Script | What it shows | Sandbox | Cost on top of tokens |
|---|---|---|---|
| `01_hosted_sandbox.py` | One call creates an agent, a sandbox, and a session. The agent writes a script, runs it, reports the real output. | `openai_hosted` | Container rate (1 GB sandbox is $0.03 per 20 min, 5 min minimum) |
| `02_function_tools.py` | Your own function tool. Handle `requires_action` by hand on turn 1, then let `sessions.stream` run the handler on turn 2. Same session, so the agent remembers turn 1. | `none` | Nothing |
| `03_subagents.py` | One flag, `multi_agent.enabled`, and the harness spawns subagents in parallel inside one sandbox. You watch them appear in the event stream. | `openai_hosted` | Container rate |

`common.py` holds the client setup and a small event printer. The harness streams around 30 event types; the printer keeps commands, tool calls, messages, subagents, and the turn end.

## Install

Requires Python 3.11 or newer and an OpenAI API key with `api.agents.read`, `api.agents.write`, and `api.responses.write` scopes (a normal project key has all three).

With uv:

```bash
cd openai_agents_058
cp .env.example .env        # then paste your key into .env
uv sync
```

With pip:

```bash
cd openai_agents_058
cp .env.example .env        # then paste your key into .env
python -m venv .venv && source .venv/bin/activate
pip install "openai>=3.14" python-dotenv
```

## Run

```bash
uv run python 01_hosted_sandbox.py
uv run python 02_function_tools.py
uv run python 03_subagents.py
```

Or with the pip venv active, `python 01_hosted_sandbox.py` and so on.

## Env vars

| Var | Where | Notes |
|---|---|---|
| `OPENAI_API_KEY` | `.env` in this folder | Loaded by `python-dotenv` in `common.py`. `.env` is gitignored at the repo root. Never commit it. |

Model is `gpt-6-astra`, set once in `common.py`.

## What to expect when you run it

Each script prints a timestamped transcript built by `Printer` in `common.py`. Lines you will see, in order:

### 01_hosted_sandbox.py

1. `session sess_... env: openai_hosted` within a few seconds.
2. A `commentary:` line where the agent says what it is about to do.
3. `READY environment` then `CONNECTED environment`. Sandbox provisioning takes roughly 20 to 30 seconds. This is the part worth pointing at on camera.
4. One or more `$ /bin/bash -lc ...` lines. The agent usually looks for `AGENTS.md` first, the same habit Codex has locally, then runs `python3 /workspace/outputs/primes.py`.
5. `final_answer:` with the script's output: the first 10 primes (2 through 29) and their sum, 129.
6. `turn done.` and the session id. Expect about a minute end to end.

### 02_function_tools.py

1. `session sess_... env: none` almost immediately. No sandbox, no container charge.
2. `tool call: lookup_member {'email': 'sam@example.com'}`. That is the `requires_action` branch in the script firing and posting the result back.
3. `final_answer:` saying Sam is a churn risk (41 days inactive, Pro plan).
4. `--- follow-up on the same session ---`, then a `final_answer:` with a short check-in message. No second tool call: the session already holds Sam's record from turn 1. That is the point of the demo.
5. Both turns together take about 40 seconds.

### 03_subagents.py

1. `session sess_... env: openai_hosted`, then the environment `READY` and `CONNECTED` lines as in demo 1.
2. Three `subagent created: <name>` lines. The harness names its subagents itself.
3. `final_answer:` with one line per job: the 20th Fibonacci number (6765), the word count (9), and pi to 8 places (3.14159265).
4. `turn done.` Expect about a minute.

Subagent shell commands run on the subagents' own turns and do not appear on the root stream. List them with `client.beta.agents.sessions.subagents.items.list(...)` if you want them on screen.

`turn.usage` may come back `None` on completed turns, so the `turn done.` line does not always carry token counts. Use the pricing page for cost numbers.

## Things worth saying on camera

- `environment: {"type": "none"}` needs `input` at create time. The API returns `conversation-only sessions currently require initial input` without it. Hosted sandboxes can be created idle.
- `sessions.create(stream=True)` is the one-call path. `sessions.stream(session_id, input=..., tool_handlers=...)` is the follow-up path and it runs your tool handlers for you. Demo 2 shows both.
- Sessions with a hosted sandbox are deleted after keep-alives stop for an hour. Store the session id if you want to come back.
- US-only data residency, no Zero Data Retention, even self-hosted. Check before pointing this at customer data.
- Self-hosting the sandbox is `npm install -g @openai/codex@alpha` then `codex exec-server --remote <url> --environment-id <id>` with a separate restricted environment key. Not in these scripts; it needs the key from the dashboard Agents tab.

## Docs

- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/quickstart
- https://developers.openai.com/api/docs/guides/agents-api/tools/functions
- https://developers.openai.com/api/docs/guides/agents-api/sessions/events
- https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted
- https://developers.openai.com/api/docs/pricing (Containers row)
