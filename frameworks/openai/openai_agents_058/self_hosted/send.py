"""Send one user message to an existing session.

Usage: python send.py <session_id> <message text...>

Run the executor first. If nothing is connected the input waits until it is.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_client  # noqa: E402

if len(sys.argv) < 3:
    sys.exit("usage: python send.py <session_id> <message text...>")

session_id = sys.argv[1]
text = " ".join(sys.argv[2:])

client = make_client()
client.beta.agents.sessions.events.create(
    session_id,
    events=[
        {
            "type": "agent.session.input.message",
            "input": [{"role": "user", "content": [{"type": "input_text", "text": text}]}],
        }
    ],
)

print("sent to", session_id)
print("  >", text)
