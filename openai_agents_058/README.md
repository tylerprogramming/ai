# OpenAI Agents API demo (video 058)

Four small scripts against the OpenAI Agents API (public beta, launched 2026-09-10). The API exposes the Codex harness as a managed service: OpenAI runs the agent loop, the sandbox, context compaction, and subagents. You send input and read events.

Each script is under 80 lines and meant to be read top to bottom on screen.

## What is in this folder

| File | Section | What it does | Read it when |
|---|---|---|---|
| `common.py` | Setup | Loads `.env`, builds the `OpenAI` client, sets `MODEL`. `Printer` turns the ~30 event types into a short timestamped transcript. `print_cost` prints a token and container estimate at the end of each run. | You want to change the model, the prices, or print more event types. |
| `01_hosted_sandbox.py` | Demo 1 | One `sessions.create(stream=True)` call: agent + hosted sandbox + session. The agent writes and runs a Python script, reports real output. | First run. Proves the API works and shows sandbox provisioning time. |
| `02_function_tools.py` | Demo 2 | Your own function tool with `environment: none`. Turn 1 handles `requires_action` by hand; turn 2 uses `sessions.stream` with `tool_handlers` on the same session. | You want the agent to call your code, and want to see session memory across turns. |
| `03_subagents.py` | Demo 3 | `multi_agent.enabled` on a hosted sandbox. The harness spawns parallel subagents; you watch them in the event stream. | You want fan-out without writing an orchestrator. |
| `04_self_hosted.py` | Demo 4 | Same create call as demo 1 with `environment: self_hosted` pointed at a folder on your disk. Prints the ids and the `codex exec-server` command to run next. | You want the commands to run on your machine, not in a container. |
| `self_hosted/` | Demo 4 kit | `create_session.py`, `send.py`, `stream.py`, `sessions.py` (list, cost, cancel, delete), a sample `workspace/`, `EXAMPLES.md` with messages to send, and a README that explains self-hosting and walks the three terminals. | Following the self-hosted demo end to end. |
| `pyproject.toml`, `uv.lock` | Deps | `openai>=3.14`, `python-dotenv`. Python 3.11+. | Installing. |
| `.env.example` | Secrets | Template for `OPENAI_API_KEY`. Copy to `.env`, never commit `.env`. | Before the first run. |
| `AGENTS.md` | Agent context | Layout, commands, rules, and the verified API shapes for any coding agent working in this folder. Read by Codex, Hermes, and (via import) Claude Code. | You ask an agent to add or change a demo. |
| `CLAUDE.md` | Agent context | `@AGENTS.md` plus two Claude Code specifics. | Same. |

Sections below: [Install](#install), [Run](#run), [Env vars](#env-vars), [What to expect](#what-to-expect-when-you-run-it), [On camera](#things-worth-saying-on-camera), [Docs](#docs).

| Script | What it shows | Sandbox | Cost on top of tokens |
|---|---|---|---|
| `01_hosted_sandbox.py` | One call creates an agent, a sandbox, and a session. The agent writes a script, runs it, reports the real output. | `openai_hosted` | Container rate (1 GB sandbox is $0.03 per 20 min, 5 min minimum) |
| `02_function_tools.py` | Your own function tool. Handle `requires_action` by hand on turn 1, then let `sessions.stream` run the handler on turn 2. Same session, so the agent remembers turn 1. No computer at all: the harness runs with nothing but your code to call. | `none` | Nothing |
| `03_subagents.py` | One flag, `multi_agent.enabled`, and the harness spawns subagents in parallel inside one sandbox. You watch them appear in the event stream. | `openai_hosted` | Container rate |
| `04_self_hosted.py` | One line changed from demo 1: the environment is a folder on your machine. OpenAI runs the loop, an executor you start runs the commands. | `self_hosted` | Nothing, the box is your own machine |

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
uv run python 04_self_hosted.py
```

Or with the pip venv active, `python 01_hosted_sandbox.py` and so on. Plain `python` without the venv active fails with `python not found` on a stock Mac; use `uv run python`.

## Self-hosted kit

`04_self_hosted.py` only creates the session. To actually run commands on your machine you need the executor connected and a way to send input and watch events. That is the `self_hosted/` folder: `create_session.py`, `send.py`, `stream.py`, `sessions.py`, a sample `workspace/` of markdown notes, and a README that explains what self-hosting is, why there are two keys, and the three-terminal run. Start there when you get to demo 4.

## Cost

Every demo ends with a `--- cost estimate ---` block from `print_cost` in `common.py`. Tokens come from `session.usage` priced at the standard short-context rate for `MODEL` (`PRICE` in `common.py`, from the pricing page). Container time is elapsed wall clock rounded up to 20-minute blocks at the 1 GB rate; demos 2 and 4 have no container. It is an estimate. The real number is on the dashboard Usage page and lags by minutes to an hour. `session.usage` is best effort and can be `None` right after a turn; `self_hosted/sessions.py cost <id>` re-checks later.

## Model and agent knobs

`MODEL` is set once in `common.py`. The `agent` dict also accepts `reasoning: {"effort": ...}` (`none` through `max`), `service_tier` (`flex` is half price, `fast` is double), and `text: {"verbosity": ...}`. If you change the model, update `PRICE` too.

## Agent context files

`AGENTS.md` at the root is the one file with the layout, commands, rules, and API shapes. `CLAUDE.md` imports it with `@AGENTS.md` because Claude Code reads only `CLAUDE.md`. Hermes reads `AGENTS.md` directly. The Codex harness that runs these sessions reads `AGENTS.md` too, which is why `self_hosted/workspace/` has its own small one telling the agent how the notes folder works. Three tools, one format.

`self_hosted/EXAMPLES.md` has a prompt for having Claude Code set up the self-hosted demo for you. It can run the scripts; it cannot make the environment key or export `CODEX_API_KEY`.

## Env vars

| Var | Where | Notes |
|---|---|---|
| `OPENAI_API_KEY` | `.env` in this folder | Loaded by `python-dotenv` in `common.py`. `.env` is gitignored at the repo root. Never commit it. |
| `CODEX_API_KEY` | Your shell, only in the terminal that runs `codex exec-server` | Demo 4 only. A separate restricted environment key from the dashboard Agents tab. Not in `.env`. See `self_hosted/README.md`. |

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

### 04_self_hosted.py

1. Three lines, right away: `session id`, `environment id`, `remote url`. The API generates all three; you do not look them up anywhere. No sandbox is provisioned. The environment sits in `pending` until something connects to it.
2. The exact `codex exec-server --remote ... --environment-id ...` command. Paste it into a second terminal with `CODEX_API_KEY` set to the environment key.
3. Start `uv run python self_hosted/stream.py <session id>` in a third terminal BEFORE the executor. It prints `watching sess_...` and waits. When the executor attaches it prints `CONNECTED environment`. That flip is the demo: the box is now your machine. The stream does not replay history, so if the executor was already connected the terminal stays quiet until the first message.
4. `uv run python self_hosted/send.py <session id> "What is in this folder?"` (quote it, zsh globs on `?`) and the `$ ...` lines you see in the stream are commands running on your disk, in the folder you passed as `workspace_directory`.
5. If the executor cannot reach the URL or the key is wrong you get `FAILED environment` instead of `CONNECTED`.
6. `uv run python self_hosted/sessions.py delete <session id>` when done, then Ctrl-C the executor and the watcher.

Subagent shell commands run on the subagents' own turns and do not appear on the root stream. List them with `client.beta.agents.sessions.subagents.items.list(...)` if you want them on screen.

`turn.usage` may come back `None` on completed turns, so the `turn done.` line does not always carry token counts. The cost block at the end re-reads the session and usually has them.

## Things worth saying on camera

- There are three environment types and the four demos cover all of them. `none` (demo 2): no computer at all, the harness only calls your function tools. `openai_hosted` (demos 1 and 3): OpenAI's container. `self_hosted` (demo 4): wherever you run `codex exec-server`.
- The sandbox partners (Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop, Vercel) are not a fourth type. They are `self_hosted` with the executor running on a box you rent from them. Cloudflare's guide, for example, creates the session with `type: self_hosted` and runs `codex exec-server` inside a Cloudflare Container. Demo 4 on your laptop is the same path with a different box.
- `environment: {"type": "none"}` needs `input` at create time. The API returns `conversation-only sessions currently require initial input` without it. Hosted sandboxes can be created idle.
- `sessions.create(stream=True)` is the one-call path. `sessions.stream(session_id, input=..., tool_handlers=...)` is the follow-up path and it runs your tool handlers for you. Demo 2 shows both.
- Sessions with a hosted sandbox are deleted after keep-alives stop for an hour. Store the session id if you want to come back.
- US-only data residency, no Zero Data Retention, even self-hosted. Check before pointing this at customer data.
- Self-hosting means OpenAI still runs the model and the loop; only the shell commands move to your machine, through `codex exec-server`. Same API, same events, different box. It needs a second restricted key for the executor because agent-written code can read whatever is in that process. Demo 4 and `self_hosted/` cover it.
- Stopping things: Ctrl-C on a demo script kills your client but the turn keeps running server side. `self_hosted/sessions.py cancel <id>` stops the turn, `delete <id>` removes the session and its environment. Hosted sessions also expire on their own after about an hour idle.
- There is no session viewer on the dashboard as far as the docs show. The API is the viewer: `sessions.retrieve`, `sessions.items.list`, `sessions.turns`. Dollars show up on the Usage page with a lag.

## Docs

- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/quickstart
- https://developers.openai.com/api/docs/guides/agents-api/tools/functions
- https://developers.openai.com/api/docs/guides/agents-api/sessions/events
- https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted
- https://developers.openai.com/api/docs/pricing (Containers row)
