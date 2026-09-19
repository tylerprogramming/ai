# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Repository Overview

This is Tyler's AI projects repository - a collection of AI agent projects, framework tutorials, and integrations. It serves as the main hub for code from his YouTube channel.

## Repository Structure

```
frameworks/           # AI framework projects (simple examples, NOT full courses)
├── agentops/        # Agent monitoring/observability
├── autogen/         # AutoGen projects (NOTE: v0.7+ uses new async API!)
├── crewai/          # CrewAI projects
├── openai/          # OpenAI SDK, Swarm, Agents
├── pydanticai/      # PydanticAI examples
└── smolagents/      # Smolagents examples

mini_projects/        # Standalone tutorial projects (formerly ai_agency series)
integrations/         # Third-party integrations (n8n, MCP, Google Drive)
tools/                # Utilities like crawl4ai (web scraper, NOT a framework)
youtube_shorts/       # Code for YouTube Shorts videos
claude_skill_agent_builder/  # Claude skill for building AI agents
```

## Current Framework Versions (September 2026)

| Framework | Version | Key Changes |
|-----------|---------|-------------|
| AutoGen | v0.7+ | **Complete rewrite!** New async API with `autogen_agentchat` |
| CrewAI | v1.15+ | Conversational flows, LLM overlay, human feedback |
| PydanticAI | v2.40+ | TypeSafeModel, realtime sessions |
| Smolagents | v1.26+ | Exa search, improved executors |

**IMPORTANT:** AutoGen v0.7+ is a breaking change from v0.2. The old `import autogen` pattern is deprecated. See `frameworks/autogen/autogen_v07_quickstart/` for current patterns.

## Key Conventions

- **Frameworks vs Courses**: This repo contains simple examples and tutorials for each framework. Full structured courses live in the separate `ai-courses` repository.
- **crawl4ai**: This is a web scraping tool/utility, NOT an AI framework. It belongs in `tools/`.
- **AgentOps**: This IS a framework (agent monitoring/observability), not just an integration.
- **mini_projects**: These are standalone tutorial projects, not a full "AI agency" - they were renamed from `ai_agency_*` series.
- **Default model**: Use `gpt-5.4-mini` as the default model in examples.

## Common Tasks

### Adding a new framework example
Place it under `frameworks/<framework_name>/` with a descriptive folder name.

### Adding a new integration
Place it under `integrations/` (e.g., `integrations/mcp_<service>/`).

### Adding YouTube Shorts code
Place it under `youtube_shorts/` with a numbered prefix.

### Using the agent-builder skill
The `claude_skill_agent_builder` can scaffold new agent projects. It supports AutoGen, CrewAI, PydanticAI, Smolagents, and OpenAI Agents.

## Dependencies

Most projects use:
- Python 3.10+
- Various AI SDKs (autogen-agentchat, crewai, openai, pydantic-ai, smolagents)
- Some projects require local LLM setup (Ollama, LM Studio)
- FFMPEG required for Whisper AI transcription

## Related Repositories

- `ai-courses` - Full structured courses (Atomic Agents, LangChain, LangGraph, etc.)
- `master-crewai-course` - Comprehensive CrewAI course
