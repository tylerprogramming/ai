"""Watch an existing session as a readable transcript.

Usage: python stream.py <session_id>

Leave this running. It shows the environment go PENDING then CONNECTED when the
executor attaches, then every command and message for each turn you send with
send.py. Ctrl-C to stop; the session stays alive.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import Printer, make_client  # noqa: E402

if len(sys.argv) != 2:
    sys.exit("usage: python stream.py <session_id>")

session_id = sys.argv[1]
client = make_client()
printer = Printer()

print("watching", session_id, "(Ctrl-C to stop)\n")
try:
    with client.beta.agents.sessions.events.stream(session_id) as events:
        for event in events:
            printer.handle(event)  # keep going after turn done; more turns may follow
except KeyboardInterrupt:
    print("\nstopped. session id:", session_id)
