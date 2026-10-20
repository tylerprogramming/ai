import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# "openai" uses OPENAI_API_KEY from .env, "local" uses the LM Studio server on your machine
LLM_BACKEND = os.getenv("LLM_BACKEND", "local")

# If USE_MEMGPT is False, then this example is a plain AutoGen group chat (user, PM and coder)
# If USE_MEMGPT is True, then we swap out the "coder" agent with an agent that has its own memory.
# NOTE: MemGPT (pymemgpt) has been discontinued and is now Letta. AutoGen v0.7 has no MemGPT agent,
# so we rebuild the idea with AutoGen's built-in ListMemory plus a "remember" tool the agent can call.
USE_MEMGPT = False


def create_model_client() -> OpenAIChatCompletionClient:
    if LLM_BACKEND == "openai":
        return OpenAIChatCompletionClient(model="gpt-5.4-mini")

    if LLM_BACKEND == "local":
        # Example using LM Studio on a local machine
        # You will have to change the parameters based on your setup.
        # LM Studio speaks the OpenAI API, so we use the OpenAI client with a custom base_url.
        # model_info is required because "local-model" isn't an OpenAI model name.
        return OpenAIChatCompletionClient(
            model="local-model",  # LM Studio uses whichever model you loaded
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",  # not needed, but can't be empty
            model_info={
                "vision": False,
                # The memory agent's "remember" tool needs a model that supports tool calling in LM Studio
                "function_calling": True,
                "json_output": False,
                "family": "unknown",
                "structured_output": False,
            },
        )

    raise ValueError(LLM_BACKEND)


async def main():
    model_client = create_model_client()

    # The user agent: runs the code the other agents write (in the "groupchat" folder)
    code_executor = LocalCommandLineCodeExecutor(work_dir="groupchat")
    user_proxy = CodeExecutorAgent(
        "User_proxy",
        code_executor=code_executor,
        description="A human admin who executes the code written by the coder.",
    )

    # The agent playing the role of the product manager (PM)
    pm = AssistantAgent(
        "Product_manager",
        model_client=model_client,
        system_message="Creative in software product ideas.",
    )

    if not USE_MEMGPT:
        # In the AutoGen example, we create an AssistantAgent to play the role of the coder
        print("AutoGen Coder")
        coder = AssistantAgent(
            "Coder",
            model_client=model_client,
        )

    else:
        # In our example, we swap this agent with a memory-powered agent.
        # ListMemory is injected into the model context on every turn, and the agent can add to it
        # with the "remember" tool (MemGPT's core idea: the agent manages its own memory).
        # ListMemory lives in-process; use ChromaDBVectorMemory if you want it to persist between runs.
        memory = ListMemory(name="coder_memory")

        async def remember(fact: str) -> str:
            """Save an important fact to your long-term memory so you can recall it later."""
            await memory.add(MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT))
            return f"Remembered: {fact}"

        coder = AssistantAgent(
            "MemGPT_coder",
            model_client=model_client,
            tools=[remember],
            memory=[memory],
            reflect_on_tool_use=True,
            system_message=f"I am a 10x engineer, trained in Python. I was the first engineer at Uber "
                           f"(which I make sure to tell everyone I work with).\n"
                           f"You are participating in a group chat with a user ({user_proxy.name}) "
                           f"and a product manager ({pm.name}).\n"
                           f"Use the remember tool to save anything important you'll need later.",
        )

    # Initialize the group chat between the user and two LLM agents (PM and coder).
    # The model picks who speaks next, like the old GroupChatManager. Stop after 12 messages (max_round=12).
    team = SelectorGroupChat(
        [user_proxy, pm, coder],
        model_client=model_client,
        termination_condition=MaxMessageTermination(12),
    )

    # Begin the group chat with a message from the user
    try:
        await Console(team.run_stream(task="Create a simple random number generator in python, that's it."))
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
