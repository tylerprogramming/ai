import asyncio
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.chromadb import (
    ChromaDBVectorMemory,
    OpenAIEmbeddingFunctionConfig,
    PersistentChromaDBVectorMemoryConfig,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

CHROMA_DB_PATH = "/tmp/chromadb"
CHROMA_COLLECTION = "autogen-rag-chroma"
DOCS_PATH = Path("./docs")  # put the .md / .txt files you want to ask questions about here
CHUNK_SIZE = 4000  # characters per chunk (roughly 1000 tokens)
OVERWRITE = False  # set to True if you want to overwrite an existing collection


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Split a document into chunks on paragraph boundaries."""
    chunks, current = [], ""
    for paragraph in text.split("\n\n"):
        if current and len(current) + len(paragraph) > chunk_size:
            chunks.append(current.strip())
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks


def docs_already_loaded() -> bool:
    """Check whether we already loaded the docs on a previous run (like get_or_create=True)."""
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    if CHROMA_COLLECTION not in [c.name for c in client.list_collections()]:
        return False
    return client.get_collection(CHROMA_COLLECTION).count() > 0


async def load_docs(memory: ChromaDBVectorMemory) -> None:
    """Chunk every document in DOCS_PATH and add the chunks to the vector memory."""
    for doc in sorted(DOCS_PATH.glob("*")):
        if doc.suffix not in (".md", ".txt"):
            continue
        for i, chunk in enumerate(chunk_text(doc.read_text(encoding="utf-8"))):
            await memory.add(
                MemoryContent(
                    content=chunk,
                    mime_type=MemoryMimeType.TEXT,
                    metadata={"source": doc.name, "chunk": i},
                )
            )
        print(f"Loaded {doc.name}")


async def main():
    # AutoGen v0.7 has no RetrieveUserProxyAgent (RetrieveChat). Instead, we give the assistant a
    # ChromaDB vector memory: before each reply, it searches the memory with the latest message and
    # adds the most relevant chunks to the model's context.
    already_loaded = docs_already_loaded()
    rag_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name=CHROMA_COLLECTION,
            persistence_path=CHROMA_DB_PATH,
            k=2,  # number of chunks to retrieve (n_results)
            score_threshold=0.4,  # ignore chunks that aren't relevant enough
            # OpenAI's text-embedding-ada-002 model is used for generating embeddings
            embedding_function_config=OpenAIEmbeddingFunctionConfig(
                api_key=os.getenv("OPENAI_API_KEY", ""),
                model_name="text-embedding-ada-002",
            ),
        )
    )

    if OVERWRITE and already_loaded:
        await rag_memory.clear()
        already_loaded = False
    if not already_loaded:
        await load_docs(rag_memory)

    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini", timeout=600)

    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        memory=[rag_memory],
        system_message="You are a helpful assistant. Answer using the relevant memory content "
                       "retrieved from the documents, plus your own knowledge.",
    )

    qa_problem = "What is Autogen Studio?  Please give a detailed overview of the project."
    # Console prints the retrieved chunks (MemoryQueryEvent) and then the assistant's answer
    await Console(assistant.run_stream(task=qa_problem))

    await rag_memory.close()
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
