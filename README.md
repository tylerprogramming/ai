# AI Projects & Learning Repository

A collection of AI agent projects, framework tutorials, and integrations.

## Repository Structure

```
├── frameworks/          # AI framework projects organized by framework
│   ├── autogen/        # 21 AutoGen projects
│   ├── crewai/         # 16 CrewAI projects  
│   ├── openai/         # OpenAI SDK, Swarm, Agents, Image Gen
│   ├── pydanticai/     # PydanticAI examples
│   └── smolagents/     # Smolagents examples
│
├── mini_projects/      # Standalone tutorial projects (formerly ai_agency series)
│   ├── 01_workout
│   ├── 02_lmstudio
│   ├── 03_video_captions
│   ├── 04_youtube_service
│   ├── 05_pdf
│   ├── 06_meal_gym_planner
│   ├── 07_news_aggregator
│   ├── 08_checklistai
│   ├── 09_movie_recommendation
│   └── 10_powerpoint_ai
│
├── integrations/       # Third-party integrations
│   ├── n8n_crewai
│   ├── n8n_runner
│   ├── mcp_crewai
│   ├── mcp_supabase
│   └── google_drive_monitor
│
├── tools/              # Utilities and tools (not frameworks)
│   ├── crawl4ai/       # Web scraping tool
│   └── repo_images/
│
└── misc/               # Other projects and experiments
    ├── claude_skill_social_me
    ├── saas_products
    └── ...
```

## Current Library Versions
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

## Need to KNOW
- MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API. I opened issue here: [https://github.com/tylerprogramming/ai/issues/1](https://github.com/cpacker/MemGPT/issues/568)
- Issues with function calling connected with LM Studio. GPT function calling works, but as soon as the config is swapped for localhost to LM Studio, they are ignored
- NEED to make sure that if using LM Studio, set the UserAgent to have a default auto reply to "..." or something. LM Studio complains about this because of the interaction
- FFMPEG: must be installed to use Whisper AI
  - MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
  - WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows

## Skills / Claude Code
- [claude_skill_social_me](misc/claude_skill_social_me) - a Claude Code skill that researches a topic across YouTube, Instagram, TikTok and X through the Apify MCP server and writes a brief on what to make next. Includes the five-line prompt that builds it.

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
