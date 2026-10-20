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

## Current Framework Versions (October 2026)

**CRITICAL:** AutoGen has completely changed its API in v0.7+!

| Framework | Package | Current Pattern |
|-----------|---------|-----------------|
| AutoGen v0.7 | `autogen-agentchat~=0.7.5`, `autogen-ext[openai]~=0.7.5` | Async, event-driven; pass `model_info` for gpt-5.4-mini |
| CrewAI v1.15 | `crewai[tools]>=1.15,<2` | Decorators, YAML config, Flows |
| PydanticAI v2 | `pydantic-ai>=2.58,<3` | `output_type`, `result.output` |
| Smolagents v1.26 | `smolagents[toolkit,litellm]>=1.26,<2` | Code agents, LiteLLM |
| OpenAI Agents SDK | `openai-agents~=0.24` | Agents, tools, handoffs |
| OpenAI SDK | `openai>=3.35,<4` | Chat completions, `chat.completions.parse`, hosted Agents API |

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

model_client = OpenAIChatCompletionClient(
    model="gpt-5.4-mini",
    # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
    model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
)
agent = AssistantAgent(name="...", model_client=model_client)
await Console(agent.run_stream(task="..."))  # from autogen_agentchat.ui import Console; or: result = await agent.run(task="...")
```

All AutoGen examples use the v0.7 API, including older ones first recorded on 0.2 (migrated in place — YouTube descriptions link to these paths, so don't move or rename project folders).

## Code Style

- Python projects typically use virtual environments
- API keys come from environment variables / `.env` (no `OAI_CONFIG_LIST` files)
- Environment variables in `.env` files (see `.env.example`)
- Most projects are standalone and self-contained
- Default model: `gpt-5.4-mini`

## When Adding New Content

1. **New framework example**: `frameworks/<framework_name>/<project_name>/`
2. **New mini project**: `mini_projects/<number>_<name>/`
3. **New integration**: `integrations/<integration_name>/`
4. **New tool**: `tools/<tool_name>/`

Every new project should include a `requirements.txt` (or `pyproject.toml`) listing its dependencies.

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
