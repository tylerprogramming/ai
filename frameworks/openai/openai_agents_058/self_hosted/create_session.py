"""Step 1: create a self-hosted session and print what the executor needs.

Usage: python create_session.py [workspace_dir]

Prints the session id, environment id, and remote_url, then the exact
codex exec-server command to run in a second terminal.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import MODEL, make_client  # noqa: E402

DEFAULT_WORKSPACE = "/Users/tylerreed/agents-demo/workspace"

workspace = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_WORKSPACE).resolve()
if not workspace.is_dir():
    sys.exit(f"workspace does not exist: {workspace}")

client = make_client()

session = client.beta.agents.sessions.create(
    agent={
        "model": MODEL,
        "instructions": (
            "You work inside the user's notes folder. Read files before answering. "
            "Only change files when asked. Be brief."
        ),
    },
    environment={"type": "self_hosted", "workspace_directory": str(workspace)},
)

env = session.environment
assert env.type == "self_hosted"

print("session id:     ", session.id)
print("environment id: ", env.id)
print("remote url:     ", env.remote_url)
print("workspace:      ", workspace)

print("\nStep 2. In another terminal, with CODEX_API_KEY set to your environment key:\n")
print(f'  codex exec-server --remote "{env.remote_url}" --environment-id "{env.id}"')

print("\nStep 3. Watch the session, then send it something:\n")
print(f"  uv run python stream.py {session.id}")
print(f"  uv run python send.py {session.id} \"What is in this folder? One line per file.\"")
