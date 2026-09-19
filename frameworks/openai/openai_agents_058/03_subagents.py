"""Demo 3: subagents, one flag.

Turn on multi_agent and the harness can split a task across subagents that run
in parallel inside the same sandbox. You watch them get created and closed in
the event stream. No orchestration code on your side.
"""

from common import MODEL, Printer, make_client, print_cost

client = make_client()
printer = Printer()

with client.beta.agents.sessions.create(
    agent={
        "model": MODEL,
        "instructions": (
            "You lead a small team. For multi-part tasks, delegate each part to a "
            "subagent, run them in parallel, then combine the results into one short answer."
        ),
        "multi_agent": {"enabled": True, "max_concurrent_subagents": 3},
    },
    environment={"type": "openai_hosted"},
    input=(
        "Three independent jobs, one subagent each: "
        "(1) write fib.py that prints the 20th Fibonacci number and run it; "
        "(2) write words.py that counts the words in the sentence 'the quick brown fox jumps over the lazy dog' and run it; "
        "(3) write pi.py that prints pi to 8 decimal places using only the math module and run it. "
        "Report the three outputs in one line each."
    ),
    stream=True,
) as events:
    for event in events:
        if printer.handle(event):
            break

print("\nsession id:", printer.session_id)
print_cost(client, printer.session_id, printer.t0)
