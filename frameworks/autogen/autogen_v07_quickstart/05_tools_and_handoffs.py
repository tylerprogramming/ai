"""
AutoGen v0.7+ Tools and Handoffs Example

Demonstrates custom tools and agent handoffs for complex workflows.
"""

import asyncio
from typing import Annotated
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, HandoffTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def search_database(query: Annotated[str, "The search query"]) -> str:
    """Search the product database."""
    products = {
        "laptop": "MacBook Pro - $1999, Dell XPS - $1599",
        "phone": "iPhone 15 - $999, Samsung S24 - $899",
        "tablet": "iPad Pro - $1099, Surface Pro - $999",
    }
    for key, value in products.items():
        if key in query.lower():
            return f"Found: {value}"
    return "No products found matching your query."


async def check_inventory(product: Annotated[str, "Product name to check"]) -> str:
    """Check product inventory."""
    return f"{product}: 15 units in stock, ready to ship within 2 days."


async def process_order(
    product: Annotated[str, "Product to order"],
    quantity: Annotated[int, "Number of items"],
) -> str:
    """Process a customer order."""
    return f"Order placed: {quantity}x {product}. Order #12345. Estimated delivery: 3-5 business days."


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    sales_agent = AssistantAgent(
        name="sales_agent",
        model_client=model_client,
        tools=[search_database, check_inventory],
        handoffs=["order_agent"],
        system_message="""You are a sales agent. Help customers find products.
        Use search_database to find products and check_inventory for availability.
        When the customer wants to order, handoff to order_agent.
        Say TERMINATE when the conversation is complete.""",
    )

    order_agent = AssistantAgent(
        name="order_agent",
        model_client=model_client,
        tools=[process_order],
        handoffs=["sales_agent"],
        system_message="""You are an order processing agent. Process customer orders.
        Use process_order to complete purchases.
        If customer needs more help with products, handoff to sales_agent.
        Say TERMINATE when order is complete.""",
    )

    termination = TextMentionTermination("TERMINATE") | HandoffTermination(target="user")

    team = Swarm(
        participants=[sales_agent, order_agent],
        termination_condition=termination,
    )

    await Console(
        team.run_stream(
            task="I'm looking for a laptop. Can you show me options and help me order one?"
        )
    )
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
