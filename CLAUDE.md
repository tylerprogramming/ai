# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Repository Overview

This is Tyler's AI projects repository - a collection of AI agent projects, framework tutorials, and integrations. It serves as the main hub for code from his YouTube channel.

## Repository Structure

```
frameworks/           # AI framework projects (simple examples, NOT full courses)
├── agentops/        # Agent monitoring/observability
├── autogen/         # AutoGen projects
├── crewai/          # CrewAI projects
├── openai/          # OpenAI SDK, Swarm, Agents
├── pydanticai/      # PydanticAI examples
└── smolagents/      # Smolagents examples

mini_projects/        # Standalone tutorial projects (formerly ai_agency series)
integrations/         # Third-party integrations (n8n, MCP, Google Drive)
tools/                # Utilities like crawl4ai (web scraper, NOT a framework)
youtube_shorts/       # Code for YouTube Shorts videos
claude_skill_social_me/  # Claude skill for social media research
```

## Key Conventions

- **Frameworks vs Courses**: This repo contains simple examples and tutorials for each framework. Full structured courses live in the separate `ai-courses` repository.
- **crawl4ai**: This is a web scraping tool/utility, NOT an AI framework. It belongs in `tools/`.
- **AgentOps**: This IS a framework (agent monitoring/observability), not just an integration.
- **mini_projects**: These are standalone tutorial projects, not a full "AI agency" - they were renamed from `ai_agency_*` series.

## Common Tasks

### Adding a new framework example
Place it under `frameworks/<framework_name>/` with a descriptive folder name.

### Adding a new integration
Place it under `integrations/` (e.g., `integrations/mcp_<service>/`).

### Adding YouTube Shorts code
Place it under `youtube_shorts/` with a numbered prefix.

## Dependencies

Most projects use:
- Python 3.10+
- Various AI SDKs (autogen, crewai, openai, etc.)
- Some projects require local LLM setup (Ollama, LM Studio)
- FFMPEG required for Whisper AI transcription

## Related Repositories

- `ai-courses` - Full structured courses (Atomic Agents, LangChain, LangGraph, etc.)
- `master-crewai-course` - Comprehensive CrewAI course
