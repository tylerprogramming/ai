# OpenAI Agents Project Template

Three variants. Pick one main.py:

- **Agents SDK** (`openai-agents`, import `agents`): recommended default. Agent loop runs locally, tools are Python functions.
- **Simple Agent**: plain Chat Completions tool loop with the `openai` SDK, no framework.
- **Agents API (hosted)**: OpenAI runs the loop and a sandbox (`client.beta.agents.sessions`, beta).

## Directory Structure

```
{project_name}/
├── README.md
├── requirements.txt
├── main.py
└── tools/
    ├── __init__.py
    └── custom_tools.py
```

## requirements.txt

```
# Agents SDK variant
openai-agents~=0.24
python-dotenv>=1.0,<2
# Simple / hosted Agents API variants instead need:
# openai>=3.35,<4
```

## tools/custom_tools.py

```python
"""Custom tools for the OpenAI agent."""


def {tool_name}({param}: {param_type}) -> str:
    """{tool_description}
    
    Args:
        {param}: {param_description}
    
    Returns:
        {return_description}
    """
    # Implementation
    return result


# Tool definitions for the OpenAI API
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "{tool_name}",
            "description": "{tool_description}",
            "parameters": {
                "type": "object",
                "properties": {
                    "{param}": {
                        "type": "{json_type}",
                        "description": "{param_description}"
                    }
                },
                "required": ["{param}"]
            }
        }
    }
]

# Map tool names to functions
TOOL_FUNCTIONS = {
    "{tool_name}": {tool_name},
}
```

## main.py (Agents SDK)

Tools are plain functions decorated with `@function_tool` (the docstring becomes the description).
With this variant, `tools/custom_tools.py` only needs the function, decorated, and no `TOOLS`/`TOOL_FUNCTIONS`.

```python
"""
{project_name} - OpenAI Agents SDK

{description}
"""

import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


@function_tool
def {tool_name}({param}: {param_type}) -> str:
    """{tool_description}"""
    # Implementation
    return result


agent = Agent(
    name="{agent_name}",
    model=os.getenv("MODEL", "gpt-5.4-mini"),
    instructions="{system_prompt}",
    tools=[{tool_name}],
)


async def main():
    task = "{default_task}"
    print(f"Running task: {task}\n")

    result = await Runner.run(agent, task)

    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

## main.py (Simple Agent)

```python
"""
{project_name} - OpenAI Agent

{description}
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools.custom_tools import TOOLS, TOOL_FUNCTIONS

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_agent(task: str) -> str:
    """Run the agent with the given task."""
    messages = [
        {"role": "system", "content": "{system_prompt}"},
        {"role": "user", "content": task},
    ]

    while True:
        # Only send `tools` when there are some (None would be sent as null)
        extra = {"tools": TOOLS} if TOOLS else {}
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-5.4-mini"),
            messages=messages,
            **extra,
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)
            
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                
                if func_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[func_name](**func_args)
                else:
                    result = f"Unknown tool: {func_name}"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
        else:
            return message.content


def main():
    task = "{default_task}"
    print(f"Running task: {task}\n")
    
    result = run_agent(task)
    
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result)


if __name__ == "__main__":
    main()
```

## main.py (Agents API - Hosted Environment)

Requires `openai>=3.35`. The session streams `agent.session.*` events.

```python
"""
{project_name} - OpenAI Agents API (hosted)

{description}
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def handle_event(event) -> bool:
    """Print agent messages and commands. Returns True when the root turn is finished."""
    t = event.type
    if t == "agent.session.turn.item.added" and event.item.type == "command_execution":
        print("$", event.item.command)
    elif t == "agent.session.turn.item.done" and event.item.type == "message":
        print("".join(c.text for c in event.item.content if c.type == "output_text"))
    elif t == "agent.session.turn.completed" and event.turn.subagent_id is None:
        return True
    elif t in ("agent.session.turn.failed", "agent.session.failed", "error"):
        print("FAILED:", event.to_json(indent=None)[:500])
        return True
    return False


def main():
    print("Starting agent session...\n")

    with client.beta.agents.sessions.create(
        agent={
            "model": os.getenv("MODEL", "gpt-5.4-mini"),
            "instructions": "{system_prompt}",
        },
        environment={"type": "openai_hosted"},
        input="{default_task}",
        stream=True,
    ) as events:
        for event in events:
            if handle_event(event):
                break

    print("\n\nSession complete.")


if __name__ == "__main__":
    main()
```

## tools/__init__.py

```python
from .custom_tools import TOOLS, TOOL_FUNCTIONS, {tool_name}

__all__ = ["TOOLS", "TOOL_FUNCTIONS", "{tool_name}"]
```

## README.md Template

```markdown
# {project_name}

{description}

## Features

- Built on the OpenAI Agents SDK (or the Chat Completions / hosted Agents API variant)
- Tool calling support

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-key"
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Tools

{tools_list}

## Customization

- Modify `tools/custom_tools.py` to add new tools
- Update the system prompt in `main.py`
- Change the model via the `MODEL` environment variable
```
