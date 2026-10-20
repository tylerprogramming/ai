# AI Projects & Learning Repository

[![YouTube](https://img.shields.io/badge/YouTube-TylerReedAI-red?style=flat&logo=youtube)](https://youtube.com/@TylerReedAI)
[![GitHub stars](https://img.shields.io/github/stars/tylerprogramming/ai?style=flat&logo=github)](https://github.com/tylerprogramming/ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A collection of AI agent projects, framework tutorials, and integrations. This is the main hub for code from my [YouTube channel](https://youtube.com/@TylerReedAI).

> **Looking for full courses?** Check out [ai-courses](https://github.com/tylerprogramming/ai-courses) for structured learning paths (LangChain, LangGraph, Atomic Agents, etc.)

## Repository Structure

```
├── frameworks/           # AI framework projects (simple examples, not full courses)
│   ├── agentops/        # Agent monitoring/observability
│   ├── autogen/         # AutoGen projects (includes v0.7+ examples)
│   ├── crewai/          # CrewAI projects (includes v1.15+ features)
│   ├── openai/          # OpenAI SDK, Swarm, Agents, Image Gen
│   ├── pydanticai/      # PydanticAI examples (includes v2.x features)
│   └── smolagents/      # Smolagents examples (includes v1.26+ features)
│
├── mini_projects/        # Standalone tutorial projects
│   ├── 00_getting_started
│   ├── 01_workout
│   ├── 02_lmstudio
│   ├── 03_video_captions
│   └── ...more
│
├── integrations/         # Third-party integrations
│   ├── google_drive_monitor
│   ├── mcp_crewai
│   ├── mcp_supabase
│   ├── n8n_crewai
│   └── n8n_runner
│
├── tools/                # Utilities (not frameworks)
│   ├── crawl4ai/        # Web scraping tool
│   └── repo_images/
│
├── youtube_shorts/       # Code for YouTube Shorts videos
│
└── claude_skill_agent_builder/  # Claude skill for building AI agents
```

## Framework Versions (October 2026)

Every project in the repo was updated and tested against these versions:

| Framework | Package / version | Highlights |
|-----------|-------------------|------------|
| **AutoGen** | `autogen-agentchat` 0.7.5 | ⚠️ Breaking change from v0.2! New async API, event-driven |
| **CrewAI** | `crewai[tools]` 1.15 | Conversational flows, LLM overlay, streaming |
| **PydanticAI** | `pydantic-ai` 2.58 | Typed outputs (`output_type`), tools with context, streaming |
| **Smolagents** | `smolagents` 1.26 | Code agents, managed agents, LiteLLM models |
| **OpenAI Agents SDK** | `openai-agents` 0.24 | Agents, tools, handoffs |
| **OpenAI Agents API** (hosted) | `openai` 3.35 | Hosted sandbox, sessions, subagents (`openai_agents_058`) |
| **AgentOps** | `agentops` 0.4 | Agent monitoring and observability |

Default model in the examples is `gpt-5.4-mini`. Image examples use `gpt-image-2.5-flare` / `-sunburst` (`gpt-image-1` shuts down 2026-10-23).

## Framework Quick Reference

### AutoGen v0.7+ (Breaking Changes!)

The old `import autogen` API is deprecated. New pattern:

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-5.4-mini",
    # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
    model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
)
agent = AssistantAgent(name="my_agent", model_client=model_client)
await agent.run_stream(task="...")
```

See `frameworks/autogen/autogen_v07_quickstart/` for examples.

All AutoGen examples in this repo use the v0.7 API. Many were first recorded on AutoGen 0.2, so the code may differ from what's on screen in older videos.

The three archived integrations in `integrations/_legacy_integrations/` (airtable, reddit, youtube-summarizer) still use AutoGen 0.2. They pin `pyautogen==0.2.35`, which installs on Python 3.10–3.12 only.

### CrewAI v1.15+

```python
from crewai import Agent, Crew, Task, LLM
from crewai.flow import Flow, listen, start
```

See `frameworks/crewai/crewai_v115_features/` for new features.

### PydanticAI v2.x

```python
from pydantic_ai import Agent

agent = Agent("openai:gpt-5.4-mini", output_type=MyModel)
result = await agent.run("...")
print(result.output)
```

See `frameworks/pydanticai/pydanticai_v2_features/` for examples.

## Skills / Claude Code

- **[agent-builder](claude_skill_agent_builder)** - A Claude Code skill that scaffolds complete AI agent projects. Give it a task and framework, get a working project with proper structure, dependencies, and best practices.

## Getting Started

### Prerequisites

- Python 3.11–3.13 (3.12 recommended; CrewAI doesn't support 3.14 yet)
- [Ollama](https://ollama.com/) (for local LLMs)
- [LM Studio](https://lmstudio.ai/) (alternative local LLM option)

### IDE Options

- [VS Code](https://code.visualstudio.com/) with Python extension
- [PyCharm](https://www.jetbrains.com/pycharm/download)
- [Cursor](https://cursor.com/) (AI-powered IDE)

### Running Examples

Most examples are standalone. Navigate to a project folder and run:

```bash
cd frameworks/crewai/crewai_first_crew
pip install -r requirements.txt
python main.py
```

## Related Repositories

| Repository | Description |
|------------|-------------|
| [ai-courses](https://github.com/tylerprogramming/ai-courses) | Full structured courses (LangChain, LangGraph, Atomic Agents) |
| [master-crewai-course](https://github.com/tylerprogramming/master-crewai-course) | Comprehensive CrewAI course |

---

<p align="center">
  <a href="https://youtube.com/@TylerReedAI">YouTube</a> •
  <a href="https://github.com/tylerprogramming">GitHub</a>
</p>
