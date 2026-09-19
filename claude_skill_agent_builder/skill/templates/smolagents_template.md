# Smolagents v1.26+ Project Template

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
smolagents>=1.26.0
litellm>=1.40.0
duckduckgo-search>=6.0.0
python-dotenv>=1.0.0
```

## tools/custom_tools.py

```python
from smolagents import Tool


class {ToolName}(Tool):
    """{tool_description}"""
    
    name = "{tool_name}"
    description = "{tool_description}"
    inputs = {
        "{param1}": {
            "type": "{param1_type}",
            "description": "{param1_description}"
        },
        "{param2}": {
            "type": "{param2_type}",
            "description": "{param2_description}"
        },
    }
    output_type = "string"

    def forward(self, {param1}: {py_type1}, {param2}: {py_type2}) -> str:
        # Implementation
        return result
```

## tools/__init__.py

```python
from .custom_tools import {ToolName}

__all__ = ["{ToolName}"]
```

## main.py (Code Agent)

```python
"""
{project_name} - Smolagents v1.26+ Code Agent

{description}
"""

import os
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel
from tools import {tool_imports}

load_dotenv()


def main():
    model = LiteLLMModel(
        model_id=os.getenv("MODEL", "gpt-5.4-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool(), {tools}],
        model=model,
        max_steps={max_steps},
    )

    task = "{default_task}"
    print(f"Running task: {task}\n")
    
    result = agent.run(task)
    
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result)


if __name__ == "__main__":
    main()
```

## main.py (Tool Calling Agent)

```python
"""
{project_name} - Smolagents Tool Calling Agent

{description}
"""

from smolagents import ToolCallingAgent, LiteLLMModel
from tools import {tool_imports}


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    agent = ToolCallingAgent(
        tools=[{tools}],
        model=model,
        max_steps={max_steps},
    )

    result = agent.run("{default_task}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
```

## Multi-Agent Template

```python
from smolagents import CodeAgent, ManagedAgent, LiteLLMModel


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    # Create specialized sub-agents
    {sub_agent1_name} = CodeAgent(
        tools=[{sub_agent1_tools}],
        model=model,
        max_steps=3,
    )

    {sub_agent2_name} = CodeAgent(
        tools=[{sub_agent2_tools}],
        model=model,
        max_steps=3,
    )

    # Wrap as managed agents
    managed_{sub_agent1_name} = ManagedAgent(
        agent={sub_agent1_name},
        name="{sub_agent1_name}",
        description="{sub_agent1_description}",
    )

    managed_{sub_agent2_name} = ManagedAgent(
        agent={sub_agent2_name},
        name="{sub_agent2_name}",
        description="{sub_agent2_description}",
    )

    # Create manager agent
    manager = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[managed_{sub_agent1_name}, managed_{sub_agent2_name}],
        max_steps={max_steps},
    )

    result = manager.run("{task}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
```

## README.md Template

```markdown
# {project_name}

{description}

## Agent Type

{agent_type_description}

## Tools

{tools_list}

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-key"
   # Or for Hugging Face:
   export HF_TOKEN="your-token"
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Using Different Models

```python
# OpenAI
model = LiteLLMModel(model_id="gpt-5.4-mini")

# Anthropic
model = LiteLLMModel(model_id="claude-3-5-sonnet-20241022")

# Hugging Face
from smolagents import HfApiModel
model = HfApiModel()
```
```
