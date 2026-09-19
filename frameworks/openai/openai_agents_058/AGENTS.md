# openai_agents_058

Demo code for a YouTube video on the OpenAI Agents API. Viewers clone this and
follow along. Every file is meant to be read on screen, so keep it short.

## Layout

- `common.py`: client setup, `MODEL`, `PRICE`, `Printer`, `print_cost`.
- `01` to `04_*.py`: one demo each, under 45 lines, docstring at the top saying
  what the demo proves.
- `self_hosted/`: the working kit for demo 4. `create_session.py`, `send.py`,
  `stream.py`, `sessions.py`, `workspace/` (sample notes), `EXAMPLES.md`.

## Commands

- Install: `uv sync`
- Run a demo: `uv run python 01_hosted_sandbox.py`
- Kit scripts run from inside `self_hosted/`: `uv run python send.py <id> "text"`
- Syntax check everything: `uv run python -m py_compile *.py self_hosted/*.py`
- Plain `python` is not on the path here. Always `uv run python`.

## Rules

- Never commit or print `.env`, `OPENAI_API_KEY`, or `CODEX_API_KEY`.
- Never run a script that calls the API unless the user asks. They cost money.
- Do not change `MODEL` or `PRICE` in `common.py` without being asked.
- Do not touch `01` to `03` when adding a new demo. New demos get a new file.
- New demos import from `common.py`. Kit scripts insert the parent dir on
  `sys.path` and import from `common` the same way `send.py` does.
- Keep the two README tables in sync when adding a file.
- Prose: short sentences, no em dashes, no hype.
- Quote shell examples that contain `?` or `*`. zsh globs them.

## API shapes (openai 3.14, verified 2026-09-17)

- Create: `client.beta.agents.sessions.create(agent={...}, environment={...}, input=..., stream=True)`
- Self-hosted env: `{"type": "self_hosted", "workspace_directory": "<abs path>"}`, no `input` at create time
- Send input: `sessions.events.create(session_id, events=[{"type": "agent.session.input.message", "input": [...]}])`
- Watch: `sessions.events.stream(session_id)` as a context manager. No replay.
- Cancel: event type `agent.session.input.cancel`. Delete: `sessions.delete(id)`.
- Executor: `codex exec-server --remote "<remote_url>" --environment-id "<env id>"` with `CODEX_API_KEY` set to a restricted environment key, never the app key.
