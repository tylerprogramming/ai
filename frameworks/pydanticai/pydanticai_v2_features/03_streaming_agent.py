"""
PydanticAI Streaming Agent Example

Real-time streaming responses from agents.
"""

from pydantic_ai import Agent


agent = Agent(
    "openai:gpt-5.4-mini",
    system_prompt="You are a creative storyteller. Write engaging, vivid stories.",
)


async def main():
    print("Streaming story generation...\n")
    print("-" * 50)

    async with agent.run_stream(
        "Write a short story about an AI that learns to paint"
    ) as response:
        async for chunk in response.stream_text():
            print(chunk, end="", flush=True)

    print("\n" + "-" * 50)
    print("\nStreaming complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
