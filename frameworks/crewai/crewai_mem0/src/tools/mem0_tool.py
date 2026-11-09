from crewai.tools import tool
from mem0 import Memory
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    # memory.add() runs an LLM to extract facts. With no "llm" block, mem0 2.2.1
    # falls back to gpt-5-mini, which OpenAI shuts down on 2026-12-11.
    "llm": {
        "provider": "openai",
        "config": {"model": "gpt-5.4-mini"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": os.getenv("QDRANT_COLLECTION_NAME"),
            "url": os.getenv("QDRANT_URL"),
            "api_key": os.getenv("QDRANT_API_KEY"),
        }
    }
}

memory = Memory.from_config(config_dict=config)

@tool("Write to Memory")
def write_to_memory(data: str) -> str:
    """Writes the given joke to the memory store"""
    user_id = "joke_agent"

    print(f"Data: {data}")

    result = memory.add(messages=data, user_id=user_id)

    return f"Memory added! {result}"


@tool("Read from Memory")
def read_from_memory(query: str) -> str:
    """Reads memories based on a query."""
    user_id = "joke_agent"

    print(f"Query: {query}")

    # mem0 2.x: scope with filters=..., results are under "results" with the text in "memory"
    memories = memory.get_all(filters={"user_id": user_id})

    print(memories)

    if memories["results"]:
        return "\n".join([mem["memory"] for mem in memories["results"]])
    else:
        return "No relevant memories found."
