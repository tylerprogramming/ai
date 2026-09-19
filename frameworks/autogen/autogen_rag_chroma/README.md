# AutoGen RAG with Chroma

This project demonstrates the use of Retrieval-Augmented Generation (RAG) with AutoGen and ChromaDB for enhanced question-answering capabilities.

## Overview

The main script `rag_01.py` sets up a RAG system using AutoGen's agents and ChromaDB as the vector database. It allows for querying information from stored documents, combining the power of large language models with the ability to retrieve relevant context from a knowledge base.

## Components

### 1. Configuration

- The script uses a configuration file `OAI_CONFIG_LIST.json` to specify the models and their API endpoints.
- Environment variables are loaded from a `.env` file.

### 2. ChromaDB Setup

- A persistent ChromaDB client is initialized with a specified path.
- A collection named "autogen-yt" is created or retrieved.

### 3. Embedding Function

- OpenAI's text-embedding-ada-002 model is used for generating embeddings.

### 4. Vector Database

- ChromaVectorDB is initialized with the ChromaDB path and the OpenAI embedding function.

### 5. Agents

Two main agents are created:

a. AssistantAgent:
   - Named "assistant"
   - Acts as a helpful AI assistant
   - Uses the specified LLM configuration

b. RetrieveUserProxyAgent:
   - Named "ragproxyagent"
   - Handles retrieval of relevant information
   - Configured with specific retrieval settings

### 6. Retrieval Configuration

The RetrieveUserProxyAgent is set up with the following key configurations:

- Task: Question-Answering (qa)
- Document sources: GitHub README and local docs folder
- Chunk token size: 2000
- Vector database: ChromaVectorDB instance
- Collection name: "autogen-yt"
- Embedding function: OpenAI's text-embedding-ada-002
- Context max tokens: 10000

### 7. Query Execution

- A sample question is defined: "What are the design goals of autogen studio? Can you go in depth with them?"
- The chat is initiated between the ragproxyagent and the assistant.
- The result is processed to display either the updated context or the final answer.

## How it Works

1. The script initializes the necessary components: ChromaDB, embedding function, and vector database.
2. Two agents are created: an AssistantAgent for general interaction and a RetrieveUserProxyAgent for handling RAG operations.
3. The RetrieveUserProxyAgent is configured to use specific documents as its knowledge base.
4. When a query is submitted, the RetrieveUserProxyAgent retrieves relevant information from the vector database.
5. This information is then used to augment the context provided to the AssistantAgent.
6. The AssistantAgent generates a response based on the augmented context and its own knowledge.
7. The final answer or updated context is displayed as the output.

## Usage

To use this system:

1. Ensure all required dependencies are installed.
2. Set up the `OAI_CONFIG_LIST.json` with your model configurations.
3. Create a `.env` file with necessary API keys (e.g., OPENAI_API_KEY).
4. Run the `rag_01.py` script.
5. The script will execute the sample query and display the result.

To ask different questions, modify the `qa_problem` variable in the script.

## Note

This setup demonstrates a basic RAG system. For production use, consider implementing error handling, optimizing retrieval settings, and expanding the knowledge base as needed.