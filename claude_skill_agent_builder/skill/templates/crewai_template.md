# CrewAI v1.15+ Project Template

## Directory Structure

```
{project_name}/
├── README.md
├── requirements.txt
├── main.py
├── crew.py
├── agents.yaml
├── tasks.yaml
└── tools/
    ├── __init__.py
    └── custom_tool.py
```

## requirements.txt

```
crewai>=1.15.0
crewai-tools>=0.17.0
python-dotenv>=1.0.0
```

## main.py

```python
"""
{project_name} - CrewAI v1.15+ Agent

{description}
"""

import os
from dotenv import load_dotenv
from crew import {CrewClass}

load_dotenv()


def main():
    inputs = {
        {inputs}
    }
    
    crew = {CrewClass}()
    result = crew.crew().kickoff(inputs=inputs)
    
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result)


if __name__ == "__main__":
    main()
```

## crew.py

```python
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Import custom tools
from tools import {tool_imports}


@CrewBase
class {CrewClass}:
    """Crew for {description}"""

    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    def __init__(self):
        self.llm = LLM(model="gpt-5.4-mini")

    @agent
    def {agent1_name}(self) -> Agent:
        return Agent(
            config=self.agents_config["{agent1_name}"],
            llm=self.llm,
            tools=[{agent1_tools}],
            verbose=True,
        )

    @agent
    def {agent2_name}(self) -> Agent:
        return Agent(
            config=self.agents_config["{agent2_name}"],
            llm=self.llm,
            tools=[{agent2_tools}],
            verbose=True,
        )

    @task
    def {task1_name}(self) -> Task:
        return Task(
            config=self.tasks_config["{task1_name}"],
        )

    @task
    def {task2_name}(self) -> Task:
        return Task(
            config=self.tasks_config["{task2_name}"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

## agents.yaml

```yaml
{agent1_name}:
  role: "{agent1_role}"
  goal: "{agent1_goal}"
  backstory: "{agent1_backstory}"

{agent2_name}:
  role: "{agent2_role}"
  goal: "{agent2_goal}"
  backstory: "{agent2_backstory}"
```

## tasks.yaml

```yaml
{task1_name}:
  description: "{task1_description}"
  expected_output: "{task1_output}"
  agent: {agent1_name}

{task2_name}:
  description: "{task2_description}"
  expected_output: "{task2_output}"
  agent: {agent2_name}
  context:
    - {task1_name}
```

## tools/custom_tool.py

```python
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class {ToolName}Input(BaseModel):
    """Input schema for {ToolName}."""
    {param}: str = Field(..., description="{param_description}")


class {ToolName}(BaseTool):
    name: str = "{tool_name}"
    description: str = "{tool_description}"
    args_schema: Type[BaseModel] = {ToolName}Input

    def _run(self, {param}: str) -> str:
        # Implementation
        return result
```

## tools/__init__.py

```python
from .custom_tool import {ToolName}

__all__ = ["{ToolName}"]
```

## README.md Template

```markdown
# {project_name}

{description}

## Agents

- **{agent1_role}**: {agent1_goal}
- **{agent2_role}**: {agent2_goal}

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-key"
   ```

3. Run the crew:
   ```bash
   python main.py
   ```

## Customization

- Edit `agents.yaml` to modify agent roles and behaviors
- Edit `tasks.yaml` to change task definitions
- Add tools in `tools/` directory
```
