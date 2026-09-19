"""
AutoGen v0.7+ Group Chat Example

Multiple agents collaborating in a selector-based group chat.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    planner = AssistantAgent(
        name="planner",
        model_client=model_client,
        system_message="""You are a planning agent. Break down tasks into steps.
        When the task is complete, say TERMINATE.""",
    )

    coder = AssistantAgent(
        name="coder",
        model_client=model_client,
        system_message="""You are a coding agent. Write clean, efficient code.
        Focus only on implementation details.""",
    )

    reviewer = AssistantAgent(
        name="reviewer",
        model_client=model_client,
        system_message="""You are a code reviewer. Review code for bugs, 
        performance issues, and best practices. Be constructive.""",
    )

    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)

    team = SelectorGroupChat(
        participants=[planner, coder, reviewer],
        model_client=model_client,
        termination_condition=termination,
    )

    await Console(
        team.run_stream(
            task="Create a Python function that calculates the Fibonacci sequence up to n terms."
        )
    )
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
