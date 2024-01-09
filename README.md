# **Repository** - AI Projects/Learning
### This repo will be helpful in understanding AutoGen providing examples including prompts and agents for SAAS products, how AutoGen works, and diving into the functionality.

## Current Library Versions:
<a href="https://github.com/microsoft/autogen/tree/main"><img src="https://img.shields.io/badge/AutoGen-0.2.3-red"/></a>
<a href="https://lmstudio.ai/"><img src="https://img.shields.io/badge/LMStudio-0.2.10-purple"/></a>
<a href="https://github.com/cpacker/MemGPT"><img src="https://img.shields.io/badge/MemGPT-0.2.11-blue"/></a>

## FFMPEG: must be installed to use Whisper AI
- MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
- WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows

## Current Issues:
- [x] MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API.  I opened issue here: [https://github.com/tylerprogramming/ai/issues/1](https://github.com/cpacker/MemGPT/issues/568)
- [ ] issues with function calling connected with LM Studio.  GPT function calling works, but as soon as the config is swapped for localhost to LM Studio, they are ignored
- [ ] NEED to make sure that if using LM Studio, set the UserAgent to have a default auto reply to "..." or something.  LM Studio complains about this because of the interaction

## Projects
1. **autogen_memgpt** - understanding integration of MemGPT into AutoGen as an AI Agent
2. **autogen_memgpt_lmstudio** - using a local llm to integrate MemGPT into AutoGen with a local server produced by LMStudio
3. **autogentest** - examples of basic usage of AutoGen
4. **autogen_functions** - updated with a previous example and new example of function calling
5. **autogen_multiple_configs** - learn how to use multiple configurations in order to use multiple models with AutoGen
6. **autogen_transcribe_video** - learn how to use AutoGen and GPT to transcribe and translate a video with functions
7. **ai_agency_01_workout_plan** - create your first agency with functions and saving the output to a .txt and .csv file
8. **ai_agency_02_lmstudio** - learn how to directly connect to any open-source llm using lm studio with a few examples
9. **autogen_webscraping** - use gpt-vision4 with AutoGen to take pictures (web scrape) and use AI to describe the web page

## Upcoming Ideas/Projects for Videos
- [x] GPT-4 Vision with AutoGen
- [ ] Video on all available Agent Types AutoGen
- [ ] AutoGen with CodeInterpreter
- [ ] AutoGen with TeachableAgent (uses Vector DB to remember conversations)
- [ ] Auto Generated Agent Chat: Hierarchy flow using select_speaker
- [ ] Updated MemGPT with new Coding Project
- [ ] AutoGen Teams, actually creating separate teams that each do a specific thing and pass on what they accomplished to the next one
- [x] Combining GPT-4 Vision with a library that can take a screenshot of a website, perhaps with stocks for example, and examine it
- [ ] Create a Sudoku Puzzle Creator/Checker with an AI WorkForce
- [x] Create WebScraper with Puppeteer
- [x] Create AutoGen with Whisper
- [x] Fitness Tracker with multiple models and LMStudio for LocalLLM
- [x] Fitness Expert Bot with Flask Server
