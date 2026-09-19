# AI Projects & Learning Repository

A collection of AI agent projects, framework tutorials, and integrations. This is the main hub for projects from my YouTube videos.

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

## Current Framework Versions

| Framework | Version | Notes |
|-----------|---------|-------|
| AutoGen | v0.7+ | **Breaking change from v0.2!** New async API |
| CrewAI | v1.15+ | Conversational flows, LLM overlay |
| PydanticAI | v2.40+ | TypeSafe, realtime sessions |
| Smolagents | v1.26+ | Exa search, improved executors |
| OpenAI Agents | v0.58+ | Hosted sandbox, streaming |

## Framework Quick Reference

### AutoGen v0.7+ (Breaking Changes!)

The old `import autogen` API is deprecated. New pattern:

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")
agent = AssistantAgent(name="my_agent", model_client=model_client)
await agent.run_stream(task="...")
```

See `frameworks/autogen/autogen_v07_quickstart/` for examples.

### CrewAI v1.15+

```python
from crewai import Agent, Crew, Task, LLM
from crewai.flow import Flow, listen, start
```

See `frameworks/crewai/crewai_v115_features/` for new features.

### PydanticAI v2.x

```python
from pydantic_ai import Agent

agent = Agent("openai:gpt-5.4-mini", result_type=MyModel)
result = await agent.run("...")
```

See `frameworks/pydanticai/pydanticai_v2_features/` for examples.

## Skills / Claude Code

- **[agent-builder](claude_skill_agent_builder)** - A Claude Code skill that scaffolds complete AI agent projects. Give it a task and framework, get a working project with proper structure, dependencies, and best practices.

## Downloads

- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/
- PyCharm Download: https://www.jetbrains.com/pycharm/download
- Visual Studio Code: https://code.visualstudio.com/

## Notes

- Full courses live in the separate `ai-courses` repository
- `crawl4ai` is a web scraping TOOL, not a framework
- AgentOps IS a framework (for agent monitoring/observability)

## Related Repositories

- [ai-courses](https://github.com/tylerprogramming/ai-courses) - Full structured courses (Atomic Agents, LangChain, LangGraph, etc.)
- [master-crewai-course](https://github.com/tylerprogramming/master-crewai-course) - Comprehensive CrewAI course
