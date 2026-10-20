# PydanticAI v2.x Project Template

## Directory Structure

```
{project_name}/
├── README.md
├── requirements.txt
├── main.py
├── agents/
│   ├── __init__.py
│   └── {agent_name}.py
├── models/
│   ├── __init__.py
│   └── schemas.py
└── tools/
    ├── __init__.py
    └── {tool_name}.py
```

## requirements.txt

```
pydantic-ai>=2.58,<3
pydantic>=2.14,<3
python-dotenv>=1.0,<2
```

## models/schemas.py

```python
from pydantic import BaseModel, Field
from typing import Optional


class {OutputModel}(BaseModel):
    """{output_description}"""
    {field1}: {type1} = Field(description="{field1_description}")
    {field2}: {type2} = Field(description="{field2_description}")
    {field3}: Optional[{type3}] = Field(default=None, description="{field3_description}")
```

## agents/{agent_name}.py

```python
from dataclasses import dataclass
from typing import Optional
from pydantic_ai import Agent, RunContext
from models.schemas import {OutputModel}


@dataclass
class {AgentDeps}:
    """Dependencies for the agent."""
    {dep1}: {dep1_type}
    {dep2}: Optional[{dep2_type}] = None


agent = Agent(
    "openai:gpt-5.4-mini",
    deps_type={AgentDeps},
    output_type={OutputModel},
    system_prompt="""{system_prompt}""",
)


@agent.tool
async def {tool_name}(
    ctx: RunContext[{AgentDeps}],
    {param}: {param_type},
) -> str:
    """{tool_description}"""
    # Access dependencies via ctx.deps
    # Implementation
    return result
```

## main.py

```python
"""
{project_name} - PydanticAI v2.x Agent

{description}
"""

import asyncio
import os
from dotenv import load_dotenv
from agents.{agent_module} import agent, {AgentDeps}

load_dotenv()


async def main():
    deps = {AgentDeps}(
        {dep1}={dep1_value},
        {dep2}={dep2_value},
    )

    result = await agent.run(
        "{default_prompt}",
        deps=deps,
    )

    print("\nResult:")
    print(f"  {field1}: {result.output.{field1}}")
    print(f"  {field2}: {result.output.{field2}}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Streaming Template

```python
async def main_streaming():
    deps = {AgentDeps}(...)

    # Structured agent (output_type set): stream partial models, then the final one.
    async with agent.run_stream("{prompt}", deps=deps) as response:
        async for partial in response.stream_output():
            print(partial)
        result = await response.get_output()
    print(f"\nFinal: {result}")


# Plain-text agent (no output_type): stream only the new text each time.
text_agent = Agent("openai:gpt-5.4-mini", system_prompt="{system_prompt}")


async def main_streaming_text():
    async with text_agent.run_stream("{prompt}") as response:
        async for chunk in response.stream_text(delta=True):
            print(chunk, end="", flush=True)
```

## Multi-Agent Template

```python
from pydantic_ai import Agent
from models.schemas import ResearchResult, ReviewResult

researcher = Agent(
    "openai:gpt-5.4-mini",
    output_type=ResearchResult,
    system_prompt="You are a thorough researcher.",
)

reviewer = Agent(
    "openai:gpt-5.4-mini",
    output_type=ReviewResult,
    system_prompt="You are a critical reviewer.",
)


async def pipeline(topic: str):
    # Research phase
    research = await researcher.run(f"Research: {topic}")
    
    # Review phase
    review = await reviewer.run(
        f"Review this research:\n{research.output.model_dump_json()}"
    )
    
    return research.output, review.output
```

## README.md Template

```markdown
# {project_name}

{description}

## Features

- Type-safe outputs using Pydantic models
- Dependency injection for runtime context
- Async/await support
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

## Output Schema

The agent returns structured data:

```python
{OutputModel}(
    {field1}: {type1},
    {field2}: {type2},
)
```
```
