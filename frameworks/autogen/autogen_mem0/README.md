# Best Buy Chatbot with Autogen and Mem0

This project demonstrates a simple chatbot for Best Buy customer service using Autogen for conversation generation and Mem0 for memory management.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Overview

The `bestbuy_basic.py` script creates a context-aware chatbot that can answer customer queries based on previous interactions. It utilizes two main libraries:

1. **Autogen**: For generating AI responses
2. **Mem0**: For storing and retrieving conversation history

## Key Components

### 1. Environment Setup

- The script uses `dotenv` to load environment variables: `OPENAI_API_KEY` and `MEM0_API_KEY`.

### 2. Autogen Agent

- An `AssistantAgent` is created with the following configuration:
  - Name: "chatbot"
  - System message: "You are a helpful AI Assistant." plus instructions to check memory first
  - Model client: `OpenAIChatCompletionClient` with `gpt-5.4-mini`
  - Tools: `search_memory` and `add_memory` (Mem0 search/add)

### 3. Mem0 Memory Client

- A `MemoryClient` is instantiated to handle conversation storage and retrieval.

### 4. Initial Conversation

- A sample conversation is added to the Mem0 memory to provide initial context.

### 5. Context-Aware Response Generation

Mem0 is exposed to the agent as two tools:
- `search_memory` searches for relevant memories using Mem0
- `add_memory` saves new details the customer shares

The agent calls `search_memory` before answering, then replies considering the retrieved context.

### 6. Interactive Loop

- The script runs a loop, allowing users to input questions (type `exit` to quit)
- For each question, it generates a context-aware response using the Autogen agent and Mem0 memory

## How It Works

1. When a user asks a question, the agent calls `search_memory` to find relevant previous interactions in the Mem0 memory.
2. The tool result is added to the agent's context alongside the new question.
3. The Autogen agent generates a response based on this context.
4. The response is printed, and the loop continues for the next user input.

This approach allows the chatbot to maintain context across multiple interactions, providing more coherent and relevant responses to user queries.

## Setup and Usage

1. Install the requirements: `pip install -r requirements.txt`.
2. Put `OPENAI_API_KEY` and `MEM0_API_KEY` (from [app.mem0.ai](https://app.mem0.ai)) in the `.env` file.
3. Run the script: `python bestbuy_basic.py`
4. Interact with the chatbot by typing your questions when prompted.