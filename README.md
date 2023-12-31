# **Repository** - ai
### This repo will be helpful in understanding AutoGen providing examples including prompts and agents for SAAS products, how AutoGen works, and diving into the functionality.

## Current Library Versions:
- memgpt: 0.2.6
- autogen: 0.2.0
- lm studio: 0.2.10

## FFMPEG: must be installed to use Whisper AI
- MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
- WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows

## Current Issues:
- [x] MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API.  I opened issue here: [https://github.com/tylerprogramming/ai/issues/1](https://github.com/cpacker/MemGPT/issues/568)

## Projects
1. **autogen_memgpt** - understanding integration of MemGPT into AutoGen as an AI Agent
2. **autogen_memgpt_lmstudio** - using a local llm to integrate MemGPT into AutoGen with a local server produced by LMStudio
3. **autogentest** - examples of basic usage of AutoGen
4. **autogen_functions** - learn how to use functions with AutoGen
5. **autogen_multiple_configs** - learn how to use multiple configurations in order to use multiple models with AutoGen
6. **autogen_transcribe_video** - learn how to use AutoGen and GPT to transcribe and translate a video with functions
7. **ai_agency_02_lmstudio** - learn how to directly connect to any open-source llm using lm studio with a few examples
8. **autogen_webscraping** - use gpt-vision4 with AutoGen to take pictures (web scrape) and use AI to describe the web page

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
- [ ] Fitness Tracker with multiple models and LMStudio for LocalLLM
- [x] Fitness Expert Bot with Flask Server
