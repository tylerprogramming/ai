"""
AutoGen v0.7+ Code Execution Example

An agent that can write and execute Python code using a Docker sandbox.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    code_executor = DockerCommandLineCodeExecutor(
        image="python:3.12-slim",
        timeout=60,
        work_dir="./code_output",
    )

    await code_executor.start()

    coder = AssistantAgent(
        name="coder",
        model_client=model_client,
        system_message="""You are a Python coding assistant. Write code in markdown code blocks.
        After your code is executed and verified, say TERMINATE.""",
    )

    executor = AssistantAgent(
        name="executor",
        model_client=model_client,
        code_executor=code_executor,
        system_message="Execute the code and report results.",
    )

    termination = TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat(
        participants=[coder, executor],
        termination_condition=termination,
    )

    try:
        await Console(
            team.run_stream(
                task="Write a Python script that generates the first 20 prime numbers and prints them."
            )
        )
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
