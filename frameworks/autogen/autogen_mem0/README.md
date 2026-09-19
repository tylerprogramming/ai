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