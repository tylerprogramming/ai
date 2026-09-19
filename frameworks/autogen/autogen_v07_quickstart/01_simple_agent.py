"""
AutoGen v0.7+ Simple Agent Example

A basic agent with a tool that demonstrates the new async API.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 73 degrees and Sunny."


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    agent = AssistantAgent(
        name="weather_agent",
        model_client=model_client,
        tools=[get_weather],
        system_message="You are a helpful assistant that can check the weather.",
        reflect_on_tool_use=True,
        model_client_stream=True,
    )

    await Console(agent.run_stream(task="What is the weather in New York?"))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
