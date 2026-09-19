# AutoGen v0.7+ Project Template

## Directory Structure

```
{project_name}/
├── README.md
├── requirements.txt
├── main.py
├── agents/
│   └── __init__.py
└── tools/
    └── __init__.py
```

## requirements.txt

```
autogen-agentchat>=0.7.0
autogen-ext[openai]>=0.7.0
python-dotenv>=1.0.0
```

## main.py

```python
"""
{project_name} - AutoGen v0.7+ Agent

{description}
"""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# Import custom tools
from tools import {tool_imports}


async def main():
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL", "gpt-5.4-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    agent = AssistantAgent(
        name="{agent_name}",
        model_client=model_client,
        tools=[{tools}],
        system_message="""{system_message}""",
        reflect_on_tool_use=True,
        model_client_stream=True,
    )

    task = "{default_task}"
    print(f"Running task: {task}")
    
    await Console(agent.run_stream(task=task))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Multi-Agent Template

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    agent1 = AssistantAgent(
        name="{agent1_name}",
        model_client=model_client,
        system_message="""{agent1_system}""",
    )

    agent2 = AssistantAgent(
        name="{agent2_name}",
        model_client=model_client,
        system_message="""{agent2_system}""",
    )

    termination = TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat(
        participants=[agent1, agent2],
        termination_condition=termination,
    )

    await Console(team.run_stream(task="{task}"))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Tool Template

```python
# tools/__init__.py
from typing import Annotated


async def {tool_name}(
    {param}: Annotated[{type}, "{description}"]
) -> str:
    """{tool_description}"""
    # Implementation
    return result
```

## README.md Template

```markdown
# {project_name}

{description}

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

## Configuration

- `MODEL`: LLM model to use (default: gpt-5.4-mini)
- `OPENAI_API_KEY`: Your OpenAI API key
```
