"""
AutoGen v0.7+ Two Agent Chat Example

Two agents collaborating: an assistant and a user proxy that can execute code.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    )

    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful assistant. Reply TERMINATE when the task is done.",
    )

    user_proxy = UserProxyAgent(
        name="user_proxy",
        description="A proxy for the user that can provide feedback.",
    )

    termination = TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat(
        participants=[user_proxy, assistant],
        termination_condition=termination,
    )

    await Console(
        # Don't put the termination word in the task itself, or the run ends immediately.
        team.run_stream(task="Tell me a joke about programming.")
    )
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
