import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

# AutoGen v0.7 has no Teachability capability. We rebuild the idea with:
#   1. a persistent ChromaDB vector memory, so what the agent learns survives between runs, and
#   2. a "remember" tool the agent calls to save new facts the user teaches it.
# Before each reply, the most relevant memories are added to the agent's context automatically.
teachability_memory = ChromaDBVectorMemory(
    config=PersistentChromaDBVectorMemoryConfig(
        collection_name="teachability",
        persistence_path="./tmp/notebook/teachability_db",  # delete this folder to reset the memory
        k=3,  # number of memories to recall
        # Uses ChromaDB's default local embedding model (downloaded on first run)
    )
)


async def remember(fact: str) -> str:
    """Save a fact, preference or piece of information the user taught you, so you remember it in future chats."""
    await teachability_memory.add(MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT))
    return f"Remembered: {fact}"


task = """
    Here is some information about me:

    1. My favorite programming language is Java
    2. My hobbies include AI, Drinking, and Futbol
    3. My birthday is March 3rd
"""

task_tweet = """
    Create an engaging tweet about Java
"""

task_check = """
    What day is my birthday?
"""


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )

    teachable_agent = AssistantAgent(
        name="teachable_agent",  # The name is flexible, but should not contain spaces to work in group chat.
        model_client=model_client,
        tools=[remember],
        memory=[teachability_memory],
        reflect_on_tool_use=True,
        system_message="You are a helpful assistant. When the user tells you something worth remembering "
                       "(facts about them, preferences, or how to do a task), save it with the remember tool. "
                       "Use the relevant memory content you are given to personalize your answers.",
    )

    # A UserProxyAgent to represent the user: you type a reply after every agent message.
    # Type "exit" to end the chat.
    user = UserProxyAgent(name="user")

    termination = TextMentionTermination("TERMINATE") | TextMentionTermination("exit", sources=["user"])
    team = RoundRobinGroupChat([teachable_agent, user], termination_condition=termination)

    # Try `task` first to teach the agent, then `task_check` in a new run to see that it remembers.
    try:
        await Console(team.run_stream(task=task_tweet))
    finally:
        await teachability_memory.close()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
