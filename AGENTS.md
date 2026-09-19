# AGENTS.md

Instructions for AI coding agents (Cursor, GitHub Copilot, Codeium, etc.) working with this repository.

## Repository Context

This is an AI projects repository containing:
- Framework examples and tutorials (AutoGen, CrewAI, OpenAI, PydanticAI, Smolagents, AgentOps)
- Standalone mini-projects for YouTube tutorials
- Third-party integrations (n8n, MCP, Google Drive)
- Utilities and tools

## Directory Structure Rules

| Directory | Purpose | What Goes Here |
|-----------|---------|----------------|
| `frameworks/<name>/` | AI framework examples | Simple examples, NOT full courses |
| `mini_projects/` | Standalone tutorials | Numbered projects (00_, 01_, etc.) |
| `integrations/` | Third-party integrations | n8n, MCP, external service connections |
| `tools/` | Utilities | Non-framework tools like crawl4ai |
| `youtube_shorts/` | Short-form content | Code for YouTube Shorts videos |

## Important Distinctions

1. **crawl4ai is a TOOL, not a framework** - It's a web scraper utility, belongs in `tools/`
2. **AgentOps IS a framework** - It's for agent monitoring/observability
3. **This repo is for examples, not courses** - Full courses live in `ai-courses` repo

## Current Framework Versions (September 2026)

**CRITICAL:** AutoGen has completely changed its API in v0.7+!

| Framework | Package | Current Pattern |
|-----------|---------|-----------------|
| AutoGen v0.7+ | `autogen-agentchat`, `autogen-ext` | Async, event-driven |
| CrewAI v1.15+ | `crewai>=1.15.0` | Decorators, YAML config, Flows |
| PydanticAI v2.x | `pydantic-ai>=2.40.0` | Type-safe, structured outputs |
| Smolagents v1.26+ | `smolagents>=1.26.0` | Code agents, LiteLLM |
| OpenAI Agents | `openai>=1.50.0` | Chat completions, tools |

### AutoGen v0.7+ Migration

**Old (v0.2 - DEPRECATED):**
```python
import autogen
agent = autogen.AssistantAgent(name="...", llm_config={...})
```

**New (v0.7+):**
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")
agent = AssistantAgent(name="...", model_client=model_client)
await agent.run_stream(task="...")
```

## Code Style

- Python projects typically use virtual environments
- Configuration files often named `OAI_CONFIG_LIST.json` for OpenAI config
- Environment variables in `.env` files (see `.env.example`)
- Most projects are standalone and self-contained
- Default model: `gpt-5.4-mini`

## When Adding New Content

1. **New framework example**: `frameworks/<framework_name>/<project_name>/`
2. **New mini project**: `mini_projects/<number>_<name>/`
3. **New integration**: `integrations/<integration_name>/`
4. **New tool**: `tools/<tool_name>/`

## Testing

Most projects are demonstration/tutorial code. Run individual Python files directly:
```bash
cd frameworks/crewai/crewai_first_crew
python main.py
```

## Common Dependencies

- `autogen-agentchat` / `autogen-ext` - Microsoft AutoGen v0.7+ framework
- `crewai` - CrewAI multi-agent framework
- `openai` - OpenAI Python SDK
- `pydantic-ai` - PydanticAI framework
- `smolagents` - HuggingFace Smolagents
- `agentops` - Agent monitoring
- `crawl4ai` - Web scraping (in tools/)
