"""Demo 4: the sandbox is your own machine.

Same create call as demo 1 with one line changed: environment is self_hosted
and points at a folder on your disk. OpenAI still runs the model and the agent
loop. The shell commands run here, through an executor (codex exec-server)
you start in another terminal with a separate restricted key. No input at
create time, because the executor has to connect before the agent can act.

Next steps live in self_hosted/README.md.
"""

from pathlib import Path

from common import MODEL, make_client

WORKSPACE = Path.home() / "agents-demo" / "workspace"

client = make_client()

session = client.beta.agents.sessions.create(
    agent={
        "model": MODEL,
        "instructions": "You work inside the user's notes folder. Be brief.",
    },
    environment={"type": "self_hosted", "workspace_directory": str(WORKSPACE)},
)

env = session.environment
assert env.type == "self_hosted"  # remote_url only exists on self_hosted
print("session id:     ", session.id)
print("environment id: ", env.id)
print("remote url:     ", env.remote_url)

print("\nIn another terminal, with CODEX_API_KEY set to your environment key:\n")
print(f'  codex exec-server --remote "{env.remote_url}" --environment-id "{env.id}"')

print("\nThen watch the session:\n")
print(f"  uv run python self_hosted/stream.py {session.id}")
