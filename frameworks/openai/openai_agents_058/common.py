"""Shared helpers for the 058 demos. Keeps each demo file short enough to read on camera."""

import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-astra"


def make_client() -> OpenAI:
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
    return OpenAI()


class Printer:
    """Turns the raw event stream into a readable transcript.

    The harness emits ~30 event types. On screen we only care about:
    commands the agent ran, text it produced, tool calls, subagents, and the turn ending.
    """

    def __init__(self) -> None:
        self.t0 = time.time()
        self.session_id: str | None = None
        self.final_text = ""

    def _stamp(self) -> str:
        return f"[{time.time() - self.t0:5.1f}s]"

    def handle(self, ev) -> bool:
        """Print one event. Returns True when the root turn is finished."""
        t = ev.type

        if t == "agent.session.created":
            self.session_id = ev.session.id
            print(self._stamp(), "session", self.session_id, "env:", ev.session.environment.type)

        elif t.startswith("agent.session.environment."):
            print(self._stamp(), t.rsplit(".", 1)[-1].upper(), "environment")

        elif t == "agent.session.turn.item.added" and ev.item.type == "command_execution":
            print(self._stamp(), "$", ev.item.command)

        elif t == "agent.session.turn.item.added" and ev.item.type == "function_call":
            print(self._stamp(), "tool call:", ev.item.name, ev.item.arguments)

        elif t == "agent.session.turn.item.done" and ev.item.type == "message":
            text = "".join(c.text for c in ev.item.content if c.type == "output_text")
            label = ev.item.phase or "message"
            print(self._stamp(), f"{label}:", text.strip())
            if ev.item.phase == "final_answer":
                self.final_text = text

        elif t == "agent.session.subagent.created":
            print(self._stamp(), "subagent created:", ev.subagent.name or ev.subagent.id)

        elif t == "agent.session.subagent.closed":
            print(self._stamp(), "subagent closed:", ev.subagent.name or ev.subagent.id)

        elif t == "agent.session.turn.completed" and ev.turn.subagent_id is None:
            u = ev.turn.usage
            if u:
                print(self._stamp(), f"turn done. tokens in={u.input_tokens} out={u.output_tokens}")
            else:
                print(self._stamp(), "turn done.")
            return True

        elif t in ("agent.session.turn.failed", "agent.session.failed", "error"):
            print(self._stamp(), "FAILED:", ev.to_json(indent=None)[:500])
            return True

        return False
