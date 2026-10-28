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
smolagents[toolkit,litellm]>=1.26,<2
python-dotenv>=1.0,<2
```

## tools/custom_tools.py

Never `eval()` a string the model passes in. For math tools, parse with `ast` and allow only
numbers and arithmetic operators.

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
from smolagents import CodeAgent, LiteLLMModel


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    # Create specialized sub-agents. A name and description make them callable
    # by the manager (ManagedAgent was removed in recent smolagents).
    {sub_agent1_name} = CodeAgent(
        tools=[{sub_agent1_tools}],
        model=model,
        max_steps=3,
        name="{sub_agent1_name}",
        description="{sub_agent1_description}",
    )

    {sub_agent2_name} = CodeAgent(
        tools=[{sub_agent2_tools}],
        model=model,
        max_steps=3,
        name="{sub_agent2_name}",
        description="{sub_agent2_description}",
    )

    # Create manager agent
    manager = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[{sub_agent1_name}, {sub_agent2_name}],
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

# Anthropic (any model id LiteLLM knows, with the provider prefix)
model = LiteLLMModel(model_id="anthropic/claude-sonnet-5-5")

# Hugging Face Inference Providers (HfApiModel was renamed)
# Always pass model_id: the smolagents 1.26 default (Qwen/Qwen3-Next-80B-A3B-Thinking)
# is not served by Inference Providers. Any chat model at
# https://router.huggingface.co/v1/models works.
from smolagents import InferenceClientModel
model = InferenceClientModel(model_id="Qwen/Qwen3-235B-A22B-Instruct-2507")
```
```
