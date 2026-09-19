# OpenAI Agents SDK Project Template

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
openai>=1.50.0
python-dotenv>=1.0.0
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
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-5.4-mini"),
            messages=messages,
            tools=TOOLS if TOOLS else None,
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

## main.py (Agents SDK - Hosted Environment)

```python
"""
{project_name} - OpenAI Agents SDK

{description}
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def handle_event(event):
    """Handle streaming events from the agent."""
    if hasattr(event, "type"):
        if event.type == "response.text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
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

- Uses OpenAI's Chat Completions API
- Tool calling support
- Streaming responses

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
