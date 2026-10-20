import asyncio
import os
from typing import Annotated

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()  # OPENAI_API_KEY and MEM0_API_KEY from .env

USER_ID = "best_buy_service_bot"

memory_client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])

conversation = [
    {"role": "assistant", "content": "Hi, I'm Best Buy's chatbot! How can I help you?"},
    {"role": "user", "content": "I just wanted to chat with you."},
    {"role": "assistant", "content": "I'm sorry to hear that. Can you provide your TV model?"},
    {"role": "user", "content": "It's a Sony - 77\" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV"},
    {"role": "assistant", "content": "Thank you for the information. Let's troubleshoot this issue..."}
]


# Tools the agent can call to use Mem0 memory.
def search_memory(query: Annotated[str, "What to look for in the customer's previous interactions"]) -> str:
    """Search the customer's previous interactions stored in Mem0."""
    results = memory_client.search(query, filters={"user_id": USER_ID})
    memories = results.get("results", []) if isinstance(results, dict) else results
    return "\n".join(m["memory"] for m in memories) or "No previous interactions found."


def add_memory(fact: Annotated[str, "A fact about the customer worth remembering"]) -> str:
    """Save a new fact about the customer to Mem0."""
    memory_client.add(messages=[{"role": "user", "content": fact}], user_id=USER_ID)
    return "Saved to memory."


async def main():
    memory_client.add(messages=conversation, user_id=USER_ID)
    print("Conversation added to memory.")

    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    )
    agent = AssistantAgent(
        "chatbot",
        model_client=model_client,
        system_message="You are a helpful AI Assistant. Before answering, use search_memory to look up "
                       "the customer's previous interactions and answer considering them. "
                       "Use add_memory to save important new details the customer shares.",
        tools=[search_memory, add_memory],
        reflect_on_tool_use=True,  # answer in plain words after the tool calls
    )

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        result = await agent.run(task=user_input)
        print("Best Buy Chatbot:", result.messages[-1].content)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
