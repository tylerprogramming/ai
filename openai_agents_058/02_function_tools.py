"""Demo 2: your tools, your session.

The agent calls a function you own. When it needs a result the session emits
requires_action; you run the function and post the result back. Then a second
message continues the SAME session, so the agent still knows the earlier answer.

No sandbox here (environment type "none"), so this is the cheapest way to run
the harness: tokens only, no container.
"""

import json

from common import MODEL, Printer, make_client

client = make_client()

TOOLS = [
    {
        "type": "function",
        "name": "lookup_member",
        "description": "Look up a Skool community member by email.",
        "parameters": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"],
            "additionalProperties": False,
        },
    }
]

MEMBERS = {
    "sam@example.com": {"name": "Sam Rivera", "plan": "pro", "joined": "2026-03-02", "last_seen_days": 41},
}


def lookup_member(args: dict) -> dict:
    member = MEMBERS.get(args["email"])
    return {"found": member is not None, "member": member}


# Turn 1: create the session with the first task and handle the tool call by hand.
printer = Printer()
with client.beta.agents.sessions.create(
    agent={
        "model": MODEL,
        "instructions": "You are a CRM assistant. Use lookup_member for member questions. Be brief.",
        "tools": TOOLS,
    },
    environment={"type": "none"},
    input="Is sam@example.com at risk of churning?",
    stream=True,
) as events:
    for event in events:
        if event.type == "agent.session.requires_action":
            for action in event.session.required_actions:
                if action.type == "function_call" and action.name == "lookup_member":
                    result = lookup_member(action.arguments)
                    client.beta.agents.sessions.events.create(
                        event.session.id,
                        events=[{
                            "type": "agent.session.input.tool_result",
                            "turn_id": action.turn_id,
                            "call_id": action.call_id,
                            "success": True,
                            "output": json.dumps(result),
                        }],
                    )
        if printer.handle(event):
            break

session_id = printer.session_id

# Turn 2: same session, so the agent remembers Sam. The stream helper runs the
# tool handler for us this time.
print("\n--- follow-up on the same session ---")
printer = Printer()
with client.beta.agents.sessions.stream(
    session_id,
    input="Draft a two-sentence check-in message to them.",
    tool_handlers={"lookup_member": lookup_member},
) as stream:
    for event in stream:
        printer.handle(event)

print("\nsession id:", session_id)
