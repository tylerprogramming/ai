# **Repository** - AI Projects/Learning
### This repo will be helpful in understanding AutoGen providing examples including prompts and agents for SAAS products, how AutoGen works, and diving into the functionality.

## Current Library Versions:
<a href="https://github.com/microsoft/autogen/tree/main"><img src="https://img.shields.io/badge/AutoGen-0.2.28-red"/></a>
<a href="https://lmstudio.ai/"><img src="https://img.shields.io/badge/LMStudio-0.2.22-purple"/></a>
<a href="https://github.com/cpacker/MemGPT"><img src="https://img.shields.io/badge/MemGPT-0.3.14-blue"/></a>

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
- 

# Best Buy Chatbot with Autogen and Mem0

This project demonstrates a simple chatbot for Best Buy customer service using Autogen for conversation generation and Mem0 for memory management.

## Overview

The `bestbuy_basic.py` script creates a context-aware chatbot that can answer customer queries based on previous interactions. It utilizes two main libraries:

1. **Autogen**: For generating AI responses
2. **Mem0**: For storing and retrieving conversation history

## Key Components

### 1. Environment Setup

- The script uses `dotenv` to load environment variables, including the OpenAI API key.

### 2. Autogen Agent

- A `ConversableAgent` is created with the following configuration:
  - Name: "chatbot"
  - System message: "You are a helpful AI Assistant."
  - LLM config: Uses the GPT-4 model
  - Code execution is disabled
  - Human input is set to "NEVER"

### 3. Mem0 Memory Client

- A `MemoryClient` is instantiated to handle conversation storage and retrieval.

### 4. Initial Conversation

- A sample conversation is added to the Mem0 memory to provide initial context.

### 5. Context-Aware Response Generation

The `get_context_aware_response` function:
- Searches for relevant memories using Mem0
- Constructs a prompt with the retrieved context and the user's question
- Generates a reply using the Autogen agent

### 6. Interactive Loop

- The script runs an infinite loop, allowing users to input questions
- For each question, it generates a context-aware response using the Autogen agent and Mem0 memory

## How It Works

1. When a user asks a question, the script searches for relevant previous interactions in the Mem0 memory.
2. It constructs a prompt that includes this context along with the new question.
3. The Autogen agent generates a response based on this context-enriched prompt.
4. The response is printed, and the loop continues for the next user input.

This approach allows the chatbot to maintain context across multiple interactions, providing more coherent and relevant responses to user queries.

## Setup and Usage

1. Ensure you have the required libraries installed: `autogen`, `mem0`, and `python-dotenv`.
2. Set up your OpenAI API key in the `.env` file.
3. Run the script: `python bestbuy_basic.py`
4. Interact with the chatbot by typing your questions when prompted.

Note: This is a basic implementation and may require further enhancements for production use.
