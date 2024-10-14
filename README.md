# **Repository** - AI Projects/Learning
### This repo will be helpful in understanding AutoGen providing examples including prompts and agents for SAAS products, how AutoGen works, and diving into the functionality.

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

## Need to KNOW:
- MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API.  I opened issue here: [https://github.com/tylerprogramming/ai/issues/1](https://github.com/cpacker/MemGPT/issues/568)
- issues with function calling connected with LM Studio.  GPT function calling works, but as soon as the config is swapped for localhost to LM Studio, they are ignored
- NEED to make sure that if using LM Studio, set the UserAgent to have a default auto reply to "..." or something.  LM Studio complains about this because of the interaction\
- FFMPEG: must be installed to use Whisper AI
  - MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
  - WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows


## Upcoming Ideas/Projects for Videos
- [x] GPT-4 Vision with AutoGen
- [ ] AutoGen with CodeInterpreter
- [x] AutoGen with TeachableAgent (uses Vector DB to remember conversations)
- [x] Auto Generated Agent Chat: Hierarchy flow using select_speaker
- [x] AutoGen Teams, actually creating separate teams that each do a specific thing and pass on what they accomplished to the next one
- [x] Combining GPT-4 Vision with a library that can take a screenshot of a website, perhaps with stocks for example, and examine it
- [ ] Create a Sudoku Puzzle Creator/Checker with an AI WorkForce
- [x] Create WebScraper with Puppeteer
- [x] Create AutoGen with Whisper
- [x] Fitness Tracker with multiple models and LMStudio for LocalLLM
- [x] Fitness Expert Bot with Flask Server
- [x] YouTube Services
- [x] Beginner Course
- [ ] Intermediate Course
- [ ] Advanced Course

## Updates:
- 05/03/2024 - added directory for frontend code saving and example .net code
- 06/02/2024 - started an integrations directory, and the first one is Airtable + AutoGen
- 10/03/2024 - updated crewai with new crew examples, changed how they are created
- 10/04/2024 - added crewai_create_a_crew and crewai_custom_tool
- 10/10/2024 - added crewai_series with 6 days of crewai examples, will add 2 more as I continue the series
- 10/14/2024 - added jupyter notebooks for crewai_series, refining some of the code as well