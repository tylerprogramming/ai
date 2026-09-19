# **Repository** - AI Projects/Learning
### This repo contains examples and projects for various AI agent frameworks including AutoGen, CrewAI, OpenAI, and more.

## Repository Structure

```
├── frameworks/          # AI framework examples organized by framework
│   ├── autogen/        # Microsoft AutoGen examples (21 projects)
│   ├── crewai/         # CrewAI examples (16 projects)
│   ├── openai/         # OpenAI SDK, Swarm, and image generation
│   └── other/          # PydanticAI, SmolAgents, Crawl4AI
│
├── projects/           # Standalone projects and applications
│   ├── ai_agency/      # AI Agency series (10 projects)
│   ├── tutorials/      # Learning examples and shorts code
│   ├── claude_skill_social_me/
│   └── item_picker/
│
├── integrations/       # Third-party integrations
│   ├── n8n_*/          # n8n workflow automation
│   ├── mcp_*/          # Model Context Protocol examples
│   └── google_drive_monitor/
│
└── utilities/          # Helper tools and resources
    ├── repo_images/
    └── saas_products/
```

## Current Library Versions:
<a href="https://github.com/microsoft/autogen/tree/main"><img src="https://img.shields.io/badge/AutoGen-0.2.36-red"/></a>
<a href="https://github.com/crewAIInc/crewAI"><img src="https://img.shields.io/badge/CrewAI-0.70.1-blue"/></a>
<a href="https://lmstudio.ai/"><img src="https://img.shields.io/badge/LMStudio-0.2.22-purple"/></a>

## Downloads
- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/
- PyCharm Download: https://www.jetbrains.com/pycharm/download
- Anaconda Download: https://www.anaconda.com/download
- Visual Studio Code: https://code.visualstudio.com/
- .NET SDK: https://dotnet.microsoft.com/en-us/download

## Framework Examples

### AutoGen (`frameworks/autogen/`)
Examples covering agent building, function calling, RAG, memory, vision, logging, and more.

### CrewAI (`frameworks/crewai/`)
Examples including flows, crews, Docker deployment, Google Calendar integration, and mem0 memory.

### OpenAI (`frameworks/openai/`)
OpenAI SDK examples, Swarm multi-agent, and image generation tools.

### Other Frameworks (`frameworks/other/`)
- **PydanticAI** - Type-safe AI agents
- **SmolAgents** - Lightweight agents
- **Crawl4AI** - Web crawling for AI

## Projects

### AI Agency Series (`projects/ai_agency/`)
Complete application examples:
1. Workout planner
2. LM Studio integration
3. Video captions
4. YouTube service
5. PDF processing
6. Meal & gym planner
7. News aggregator
8. Checklist AI
9. Movie recommendation
10. PowerPoint AI

### Skills / Claude Code
- [claude_skill_social_me](projects/claude_skill_social_me) - A Claude Code skill that researches topics across YouTube, Instagram, TikTok and X through the Apify MCP server.

## Need to KNOW:
- MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API. [Issue #568](https://github.com/cpacker/MemGPT/issues/568)
- Issues with function calling connected with LM Studio. GPT function calling works, but as soon as the config is swapped for localhost to LM Studio, they are ignored.
- NEED to make sure that if using LM Studio, set the UserAgent to have a default auto reply to "..." or something. LM Studio complains about this because of the interaction.
- FFMPEG: must be installed to use Whisper AI
  - MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
  - WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows

## Upcoming Ideas/Projects for Videos
- [x] crewai_flow_workout
- [ ] crewai_flow_single_llm
- [ ] crewai_infographic_creation
- [ ] crewai_docker_example
- [ ] crewai_flow_recipes
- [ ] google agent sdk
- [ ] mem0 with crewai
- [ ] full local agent setup (ollama, crewai, qdrant docker, crawl4ai, postgres docker)
- [ ] don't 'vibe' code
- [ ] Find best videos from last two weeks
- [ ] Why AI is difficult...
- [ ] 5 AI Agent Projects
- [ ] agentstack
- [ ] Lovable 2.0
- [ ] bolt.new + supabase
- [ ] replit 2.0
- [ ] ag2
- [ ] letta.ai course
- [ ] .af files
