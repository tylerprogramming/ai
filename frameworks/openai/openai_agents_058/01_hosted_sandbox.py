"""Demo 1: the harness as an API.

One call creates an agent, a sandbox, and a session, then streams the agent
writing a script, running it, and reporting the real output. OpenAI runs the
loop. You never see a tool-call round trip.
"""

from common import MODEL, Printer, make_client

client = make_client()
printer = Printer()

with client.beta.agents.sessions.create(
    agent={
        "model": MODEL,
        "instructions": "Write clean code, run it, and report the actual output. Be brief.",
    },
    environment={"type": "openai_hosted"},
    input=(
        "Create primes.py that prints the first 10 prime numbers and their sum. "
        "Run it and show me the output."
    ),
    stream=True,
) as events:
    for event in events:
        if printer.handle(event):
            break

print("\nsession id:", printer.session_id)
