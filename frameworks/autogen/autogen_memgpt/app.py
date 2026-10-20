import asyncio
import os
from typing import Annotated

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()  # OPENAI_API_KEY (and optionally use_memgpt=1) from .env

CODER_SYSTEM_MESSAGE = (
    "I am a 10x engineer, trained in Python. I was the first engineer at Uber "
    "(which I make sure to tell everyone I work with).\n"
    "You are participating in a group chat with a user (User_proxy) "
    "and a product manager (Product_manager). Write code in markdown code blocks; "
    "Code_executor runs them."
)


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        seed=42,
        timeout=600,
    )

    # The user agent: a human admin. Type a reply when it's your turn, or "exit" to end the chat.
    user_proxy = UserProxyAgent("User_proxy", description="A human admin.")

    # In 0.2 the user proxy also ran the code. In v0.7 a separate agent does that.
    # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
    code_executor = LocalCommandLineCodeExecutor(work_dir="groupchat", cleanup_temp_files=False)
    executor = CodeExecutorAgent(
        "Code_executor", code_executor=code_executor,
        description="Runs the Python code that the Coder writes and reports the output.",
    )

    # The agent playing the role of the product manager (PM)
    pm = AssistantAgent(
        name="Product_manager",
        model_client=model_client,
        system_message="Creative in software product ideas.",
        description="Creative in software product ideas.",
    )

    if not os.getenv("use_memgpt"):
        coder = AssistantAgent(
            name="Coder",
            model_client=model_client,
            system_message=CODER_SYSTEM_MESSAGE,
            description="A Python engineer who writes the code.",
        )
    else:
        # MemGPT (pymemgpt) is discontinued; the project lives on as Letta (https://www.letta.com).
        # Here we rebuild the core idea with AutoGen's own memory: the coder gets a memory store
        # that is added to its context on every turn, plus a `remember` tool to save new facts into it.
        coder_memory = ListMemory(name="coder_memory")

        async def remember(fact: Annotated[str, "A fact worth keeping for the rest of the project"]) -> str:
            """Save a fact (a requirement, decision or preference) to long-term memory."""
            await coder_memory.add(MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT))
            return f"Remembered: {fact}"

        coder = AssistantAgent(
            name="MemGPT_coder",
            model_client=model_client,
            system_message=CODER_SYSTEM_MESSAGE
            + "\nUse the remember tool to save important requirements and decisions.",
            description="A Python engineer with long-term memory who writes the code.",
            memory=[coder_memory],
            tools=[remember],
            reflect_on_tool_use=True,
        )

    # Initialize the group chat between the user and the LLM agents (PM and coder).
    # The model picks who speaks next; end after 12 messages (max_round=12 in 0.2) or when the user types "exit".
    termination = MaxMessageTermination(12) | TextMentionTermination("exit", sources=["User_proxy"])
    team = SelectorGroupChat(
        [user_proxy, pm, coder, executor],
        model_client=model_client,
        termination_condition=termination,
    )

    # Begin the group chat with a message from the user
    try:
        await Console(team.run_stream(
            task="Can you make a simple flask application that has a button in the middle and generates a random "
                 "number on the screen when it's clicked?"
        ))
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
