from crewai_tools import tool
from mem0 import Memory
from dotenv import load_dotenv
import os

load_dotenv()

# Optionally configure mem0 to use any other store
# https://docs.mem0.ai/components/vectordbs/config#config
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "url": "url",
            "api_key": "api_key",
            # "port": "6333",
        }
    }
}

memory = Memory.from_config(config_dict=config)

@tool("Write to Memory")
def write_to_memory(data: str) -> str:
    """Writes the given joke to the memory store"""
    user_id = "joke_agent"
    result = memory.add(messages=data, user_id=user_id)

    return f"Memory added! {result}"


@tool("Read from Memory")
def read_from_memory(query: str) -> str:
    """Reads memories based on a query."""
    memories = memory.search(query=query)
    if memories["memories"]:
        return "\n".join([mem["data"] for mem in memories["memories"]])
    else:
        return "No relevant memories found."
