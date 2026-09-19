# Self-hosted kit

## What self-hosting means, in plain terms

In demos 1 and 3 the agent's shell commands run inside a container OpenAI spins
up for you. In this demo they run on your own machine instead.

OpenAI still runs the brain: the model, the agent loop, deciding what command
to run next. You run a small program called the executor (`codex exec-server`)
that sits in a terminal, holds an outbound connection to OpenAI, receives each
command, runs it in the folder you chose, and sends the result back.

So the split is:

| Piece | Where it runs |
|---|---|
| Model and agent loop | OpenAI |
| Session state and events | OpenAI |
| Shell commands, file reads and writes | Your machine, via the executor |

The API calls in your Python are the same as demo 1 with one line changed:
`environment` is `self_hosted` and points at a folder. There is no container
charge. Tokens only.

The sandbox partners OpenAI lists (Blaxel, Cloudflare, Daytona, DigitalOcean,
E2B, Modal, Oracle, Runloop, Vercel) are this same path. Their guides create
the session with `type: self_hosted` and run `codex exec-server` inside a
container they host. The executor, the restricted key, and the outbound
connection are identical. Only the box changes: your laptop here, their
compute there. Learn it once on your own machine and the partner version is
a deploy step.

## Two keys, and why

Two programs talk to OpenAI, so there are two keys.

1. Your Python scripts (`create_session.py`, `send.py`, `stream.py`,
   `sessions.py`). They use your normal API key, already in `.env` in the parent
   folder. It needs `api.agents.read`, `api.agents.write`, and
   `api.responses.write`. A default project key has all three.

2. The executor. It also needs a key to connect. But the agent's commands run
   right next to it, and code the agent writes could read that key. So OpenAI
   makes you use a second, weaker key there. It can do one thing: connect an
   environment. It cannot create sessions, call models, or read anything.

Make the second key on platform.openai.com, Agents tab, create an environment
key. Set every other permission to None. Copy it once. It goes in your shell
as `CODEX_API_KEY` right before you start the executor. It does not go in
`.env`, because `.env` is what the Python scripts read and they need the
normal key.

## Setup, once

```bash
npm install -g @openai/codex@alpha     # provides codex exec-server
codex exec-server --help
mkdir -p ~/agents-demo && cp -r workspace ~/agents-demo/workspace
```

`workspace/` holds six small markdown notes and an `AGENTS.md` that tells the
agent how the folder works. The Codex harness reads that file before acting,
same as Codex CLI does locally. Copying the folder out of the repo lets
the agent edit files without dirtying git. The parent folder must already be
installed (`uv sync`) with `OPENAI_API_KEY` in `.env`.

Alpha is a moving tag. To land on the exact build used in the video:
`npm install -g @openai/codex@0.156.0-alpha.7`.

## The run: three terminals

Every script below is run with `uv run python`. Plain `python` will not find
the packages unless you activate `.venv` first.

### Terminal 1: create the session

```bash
cd self_hosted
uv run python create_session.py ~/agents-demo/workspace
```

Prints three values the API generated: session id, environment id, and
remote url. Below them, the exact `codex exec-server` command with those
values filled in, and the `stream.py` command. You copy from here. Nothing
is running yet.

### Terminal 3: start watching first

```bash
cd self_hosted
uv run python stream.py <session id>
```

Prints `watching sess_...` and then waits. Start this before the executor.
The stream only shows events from the moment you connect; it does not replay
history. If the executor is already attached when you start watching, you
missed the `CONNECTED` line and the terminal sits quiet until the first
message.

### Terminal 2: start the executor

```bash
export CODEX_API_KEY=...   # the environment key, not the app key
codex exec-server --remote "<remote url>" --environment-id "<environment id>"
```

Paste the line from terminal 1 as-is. The executor registers and then sits
there. Terminal 3 should print `CONNECTED environment`. `FAILED environment`
means the key, the URL, or the executor version.

All executor connections are outbound. Nothing listens on your machine, no
port opens. If the connection drops, it reconnects on its own.

### Terminal 1 again: send work

```bash
uv run python send.py <session id> "What is in this folder? One line per file."
uv run python send.py <session id> 'Add "buy stamps" to the to-do list.'
cat ~/agents-demo/workspace/todo.md
```

Quote the message. zsh treats `?` and `*` as globs and errors with
`no matches found` if you leave them bare.

Terminal 3 shows `$ ...` lines for each command and `final_answer:` for the
reply. After the second message, `todo.md` on your disk has the new line.
More messages, including ones that exercise `workspace/AGENTS.md`, are in
`EXAMPLES.md`.

### Cleanup

```bash
uv run python sessions.py cost <session id>
uv run python sessions.py delete <session id>
```

Then Ctrl-C terminals 2 and 3. `sessions.py list` shows recent sessions
and their status if you lose an id.

## Notes

- `workspace_directory` must be an absolute path that exists on the machine
  running the executor. `create_session.py` resolves and checks it.
  `04_self_hosted.py` in the parent folder does not.
- One executor serves one environment id. New session, new executor.
- Ctrl-C on `stream.py` only stops watching. Ctrl-C on the executor puts the
  environment back to pending; the session survives.
- Every run of `create_session.py` makes a new session with new ids. Use the
  most recent set.
- Data residency is US-only and there is no Zero Data Retention, even
  self-hosted. Do not point this at customer data.
