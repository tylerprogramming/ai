# Examples

Messages to send once the executor is connected. Each line is a full command.
Replace `<id>` with your session id. Quote the text; zsh globs on `?`.

## Read

```bash
uv run python send.py <id> "What is in this folder? One line per file."
uv run python send.py <id> "What is still open on the to-do list?"
uv run python send.py <id> "Who has action items from the last meeting, and what are they?"
```

The stream shows `$ ls`, `$ cat ...`, then `final_answer:`. Nothing changes on
disk.

## Combine across files

```bash
uv run python send.py <id> "Which of the two ideas could I ship this weekend? Pick one and say why in three sentences."
uv run python send.py <id> "Cross-check the grocery list against the recipe idea. What is missing for a basic dinner?"
```

## Write

```bash
uv run python send.py <id> 'Add "buy stamps" to the to-do list.'
uv run python send.py <id> "Check off the library books item."
uv run python send.py <id> "Add eggs, butter, and flour to groceries if they are not already there."
```

Then `cat ~/agents-demo/workspace/todo.md` on your side. The edit landed on
your disk, not in a container.

## Create

```bash
uv run python send.py <id> "Write weekly-review.md summarizing open to-dos, unfinished meeting action items, and the two ideas in one paragraph each."
```

## Run something

```bash
uv run python send.py <id> "Write count.py that prints how many markdown files are here and how many total lines. Run it and show the output."
```

This is the demo 1 task, but the script runs on your machine. Delete
`count.py` afterwards or leave it; either is fine for the video.

## The AGENTS.md moment

`workspace/AGENTS.md` tells the agent how the folder works: to-dos go at the
bottom as `- [ ] item`, never delete lines, do not edit past meetings. The
Codex harness reads that file before it acts. Try:

```bash
uv run python send.py <id> "Delete the meeting note, it is old."
```

It should refuse or ask, citing the rule. Same file format Codex CLI uses
locally, and the same one Hermes reads. That is worth a sentence on camera.

## Have Claude Code drive it

The repo root has `CLAUDE.md` (which imports `AGENTS.md`), so Claude Code
already knows the layout and the rules. From the repo folder:

```bash
claude
```

Then:

```
Set up the self-hosted demo. Copy the sample workspace to ~/agents-demo,
create a session pointed at it, and give me the exec-server command.
Then start stream.py in the background and tell me when it connects.
```

Claude Code can run `create_session.py` and `stream.py`. It cannot make the
environment key on the dashboard or export `CODEX_API_KEY` into your shell.
Those two steps stay with you. Once the executor is up, you can also ask
Claude Code to send the messages above with `send.py`.

Hermes reads the same `AGENTS.md`, so a Hermes session in this folder gets the
same context without any extra file.
