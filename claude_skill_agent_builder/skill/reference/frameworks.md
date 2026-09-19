# AI Agent Frameworks Reference

Current API patterns and best practices for each supported framework.
Last updated: September 2026

---

## AutoGen v0.7+

**Major breaking change from v0.2!** The v0.7+ version is a complete rewrite.

### Installation

```bash
pip install -U "autogen-agentchat>=0.7.0" "autogen-ext[openai]>=0.7.0"
```

### Key Changes from v0.2

| Old (v0.2) | New (v0.7+) |
|------------|-------------|
| `import autogen` | `from autogen_agentchat import ...` |
| Synchronous | Async/await pattern |
| `config_list` | `OpenAIChatCompletionClient` |
| `initiate_chat()` | `agent.run()` or `run_stream()` |

### Current Pattern

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")
    
    agent = AssistantAgent(
        name="my_agent",
        model_client=model_client,
        tools=[my_tool],
        system_message="You are a helpful assistant.",
    )
    
    await Console(agent.run_stream(task="Do something"))
    await model_client.close()

asyncio.run(main())
```

### Multi-Agent Pattern

```python
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat, Swarm
from autogen_agentchat.conditions import TextMentionTermination

team = RoundRobinGroupChat(
    participants=[agent1, agent2],
    termination_condition=TextMentionTermination("TERMINATE"),
)
await team.run_stream(task="...")
```

---

## CrewAI v1.15+

### Installation

```bash
pip install -U "crewai>=1.15.0" "crewai-tools>=0.17.0"
```

### Project Structure

```
project/
├── main.py
├── crew.py
├── agents.yaml
├── tasks.yaml
└── tools/
    └── custom_tool.py
```

### Current Pattern (Decorator Style)

```python
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyCrew:
    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

### Flows (New in v1.15+)

```python
from crewai.flow import Flow, listen, start

class MyFlow(Flow):
    @start()
    def begin(self):
        return "started"

    @listen(begin)
    def next_step(self, previous):
        return self.crew.kickoff()
```

### YAML Config

**agents.yaml:**
```yaml
researcher:
  role: Senior Researcher
  goal: Find accurate information
  backstory: Expert with 10 years experience
```

**tasks.yaml:**
```yaml
research_task:
  description: Research {topic}
  expected_output: Comprehensive report
  agent: researcher
```

---

## PydanticAI v2.x

### Installation

```bash
pip install -U "pydantic-ai>=2.40.0"
```

### Current Pattern

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class OutputModel(BaseModel):
    result: str
    confidence: float

agent = Agent(
    "openai:gpt-5.4-mini",
    result_type=OutputModel,
    system_prompt="You are a helpful assistant.",
)

async def main():
    result = await agent.run("Do something")
    print(result.data)  # OutputModel instance
```

### Tools with Context

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    user_id: str

agent = Agent("openai:gpt-5.4-mini", deps_type=MyDeps)

@agent.tool
async def my_tool(ctx: RunContext[MyDeps], query: str) -> str:
    return f"Result for user {ctx.deps.user_id}"
```

### Streaming

```python
async with agent.run_stream("...") as response:
    async for chunk in response.stream_text():
        print(chunk, end="")
```

---

## Smolagents v1.26+

### Installation

```bash
pip install -U "smolagents>=1.26.0"
```

### Current Pattern

```python
from smolagents import CodeAgent, ToolCallingAgent, LiteLLMModel

model = LiteLLMModel(model_id="gpt-5.4-mini")

# Code agent - writes and executes Python
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=5,
)

# Tool calling agent - uses tools directly
agent = ToolCallingAgent(
    tools=[...],
    model=model,
)

result = agent.run("Do something")
```

### Custom Tools

```python
from smolagents import Tool

class MyTool(Tool):
    name = "my_tool"
    description = "Does something useful"
    inputs = {
        "query": {"type": "string", "description": "The query"}
    }
    output_type = "string"

    def forward(self, query: str) -> str:
        return f"Result: {query}"
```

### Multi-Agent

```python
from smolagents import ManagedAgent

managed = ManagedAgent(
    agent=sub_agent,
    name="researcher",
    description="Searches the web",
)

manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed],
)
```

---

## OpenAI Agents SDK v0.58+

### Installation

```bash
pip install -U "openai-agents>=0.58"
```

### Current Pattern

```python
from openai import OpenAI

client = OpenAI()

with client.beta.agents.sessions.create(
    agent={
        "model": "gpt-5.4-mini",
        "instructions": "You are a helpful assistant.",
    },
    environment={"type": "openai_hosted"},
    input="Do something",
    stream=True,
) as events:
    for event in events:
        # Handle streaming events
        pass
```

---

## Choosing a Framework

| Need | Best Choice |
|------|-------------|
| Multi-agent conversations | AutoGen |
| Team-based workflows | CrewAI |
| Type-safe outputs | PydanticAI |
| Lightweight code execution | Smolagents |
| Simple OpenAI integration | OpenAI Agents |
| Production deployment | CrewAI (has platform) |
| Research/experimentation | AutoGen or Smolagents |
