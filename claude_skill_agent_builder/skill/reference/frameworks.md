# AI Agent Frameworks Reference

Current API patterns and best practices for each supported framework.
Last updated: October 2026

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
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    )
    
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
pip install -U "crewai[tools]>=1.15,<2"
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

### Flows

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
pip install -U "pydantic-ai>=2.58,<3"
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
    output_type=OutputModel,  # `result_type` was removed
    system_prompt="You are a helpful assistant.",
)

async def main():
    result = await agent.run("Do something")
    print(result.output)  # OutputModel instance (`result.data` was removed)
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
# Text agent (no output_type). stream_text() yields the full text so far by default;
# delta=True yields only the new piece.
async with agent.run_stream("...") as response:
    async for chunk in response.stream_text(delta=True):
        print(chunk, end="")

# Structured agent: stream partial models, then the final one
async with structured_agent.run_stream("...") as response:
    async for partial in response.stream_output():
        print(partial)
    final = await response.get_output()
```

---

## Smolagents v1.26+

### Installation

```bash
pip install -U "smolagents[toolkit,litellm]>=1.26,<2"   # toolkit = DuckDuckGoSearchTool (ddgs), litellm = LiteLLMModel
```

### Current Pattern

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, ToolCallingAgent, LiteLLMModel

model = LiteLLMModel(model_id="gpt-5.4-mini")  # gpt-5 models: smolagents drops `stop` automatically

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

`ManagedAgent` was removed. Give the sub-agent a `name` and `description` and pass it directly:

```python
researcher = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    name="researcher",
    description="Searches the web",
)

manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[researcher],
)
```

### Custom tool safety

Never `eval()` model-supplied strings inside a tool. For math, parse with `ast` and allow only
numbers and arithmetic operators (see `frameworks/smolagents/smolagents_v126_features/03_custom_tool.py`).

---

## OpenAI Agents

Two different things share the name. Pick one:

- **OpenAI Agents SDK** (`pip install openai-agents`, import `agents`): an open-source Python
  framework. Your process runs the agent loop and your Python functions are the tools.
- **OpenAI Agents API** (hosted, beta; part of the `openai` SDK as `client.beta.agents`): OpenAI runs
  the agent loop, sandbox and subagents. You create a session and read events.

### Agents SDK (openai-agents 0.24+)

```bash
pip install -U "openai-agents~=0.24"
```

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Sunny in {city}"

agent = Agent(
    name="assistant",
    model="gpt-5.4-mini",
    instructions="You are a helpful assistant.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tampa?")
    print(result.final_output)

asyncio.run(main())
```

Multi-agent: `handoffs=[other_agent]` on an `Agent`, or `other_agent.as_tool(tool_name=..., tool_description=...)`.

### Agents API (hosted, openai 3.35+)

```bash
pip install -U "openai>=3.35,<4"
```

```python
from openai import OpenAI

client = OpenAI()

with client.beta.agents.sessions.create(
    agent={
        "model": "gpt-5.4-mini",
        "instructions": "You are a helpful assistant.",
    },
    environment={"type": "openai_hosted"},  # or {"type": "none"}, or {"type": "self_hosted", "workspace_directory": "/abs/path"}
    input="Do something",
    stream=True,
) as events:
    for event in events:
        if event.type == "agent.session.turn.item.done" and event.item.type == "message":
            print("".join(c.text for c in event.item.content if c.type == "output_text"))
        elif event.type == "agent.session.turn.completed" and event.turn.subagent_id is None:
            break
        elif event.type in ("agent.session.turn.failed", "agent.session.failed", "error"):
            break
```

Function tools go in `agent["tools"]` as `{"type": "function", "name", "description", "parameters"}`.
Follow-up turns on the same session: `client.beta.agents.sessions.stream(session_id, input=..., tool_handlers={"name": fn})`.
See `frameworks/openai/openai_agents_058/` for full examples.

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
