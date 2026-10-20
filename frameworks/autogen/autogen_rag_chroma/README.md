# AutoGen RAG with Chroma

This project demonstrates the use of Retrieval-Augmented Generation (RAG) with AutoGen and ChromaDB for enhanced question-answering capabilities.

> **Note:** Updated to AutoGen v0.7. The original video used the older AutoGen 0.2 API (`RetrieveUserProxyAgent` / RetrieveChat, which v0.7 no longer has), so the code here differs from what's on screen. The same idea is rebuilt with AutoGen's `ChromaDBVectorMemory`.

## Overview

The main script `rag_01.py` sets up a RAG system using an AutoGen agent and ChromaDB as the vector database. It allows for querying information from stored documents, combining the power of large language models with the ability to retrieve relevant context from a knowledge base.

## Components

### 1. Configuration

- The model client is `OpenAIChatCompletionClient(model="gpt-5.4-mini", model_info=...)`.
- Environment variables (`OPENAI_API_KEY`) are loaded from a `.env` file.

### 2. Documents

- Every `.md` / `.txt` file in the `docs` folder is split into chunks on paragraph boundaries (about 4000 characters each).
- `docs/autogen_README.md` is a saved copy of the AutoGen GitHub README, which the original example downloaded from GitHub.

### 3. ChromaDB vector memory

- `ChromaDBVectorMemory` stores the chunks in a persistent ChromaDB database at `/tmp/chromadb`, in a collection named "autogen-rag-chroma".
- OpenAI's text-embedding-ada-002 model is used for generating embeddings.
- The documents are only loaded on the first run; set `OVERWRITE = True` to reload them.

### 4. Agent

- An `AssistantAgent` named "assistant" with the vector memory attached (`memory=[rag_memory]`).
- Before each reply, the memory searches for the 2 most relevant chunks (`k=2`, `score_threshold=0.4`) and adds them to the model's context. This replaces the 0.2 `RetrieveUserProxyAgent`.

### 5. Query Execution

- A sample question is defined: "What is Autogen Studio?  Please give a detailed overview of the project."
- The console shows the retrieved chunks (`MemoryQueryEvent`) and then the assistant's answer.

## How it Works

1. The script creates the ChromaDB vector memory with the OpenAI embedding function.
2. On the first run, it chunks the documents in `docs` and adds them to the memory.
3. An AssistantAgent is created with the memory attached.
4. When a query is submitted, the memory retrieves relevant chunks from the vector database.
5. This information is then used to augment the context provided to the AssistantAgent.
6. The AssistantAgent generates a response based on the augmented context and its own knowledge.

## Usage

To use this system:

1. Install the dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your `OPENAI_API_KEY`.
3. Put the documents you want to ask about in the `docs` folder (`.md` or `.txt`).
4. Run `python rag_01.py`.
5. The script will execute the sample query and display the result.

To ask different questions, modify the `qa_problem` variable in the script.

## Note

This setup demonstrates a basic RAG system. For production use, consider implementing error handling, optimizing retrieval settings, and expanding the knowledge base as needed.