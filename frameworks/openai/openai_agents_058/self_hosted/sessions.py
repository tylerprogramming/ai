"""Session housekeeping for the self-hosted demo.

Usage:
  python sessions.py list                 recent sessions, newest first
  python sessions.py cost <session_id>    token cost so far (no container on self_hosted)
  python sessions.py cancel <session_id>  stop the active turn, keep the session
  python sessions.py delete <session_id>  delete the session and its environment
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_client, print_cost  # noqa: E402

USAGE = __doc__.strip()

if len(sys.argv) < 2:
    sys.exit(USAGE)

cmd, args = sys.argv[1], sys.argv[2:]
client = make_client()
sessions = client.beta.agents.sessions

if cmd == "list":
    for s in sessions.list(limit=20, order="desc"):
        when = datetime.fromtimestamp(s.created_at).strftime("%H:%M:%S")
        print(f"{s.id}  {s.status:15} {s.environment.type:14} {when}")

elif cmd == "cost" and args:
    s = sessions.retrieve(args[0])
    print_cost(client, s.id, s.created_at)

elif cmd == "cancel" and args:
    sessions.events.create(args[0], events=[{"type": "agent.session.input.cancel"}])
    print("cancel sent to", args[0])

elif cmd == "delete" and args:
    sessions.delete(args[0])
    print("deleted", args[0])

else:
    sys.exit(USAGE)
