"""
Smolagents Multi-Agent Example

Hierarchical multi-agent system with a manager agent.
"""

from smolagents import CodeAgent, ManagedAgent, DuckDuckGoSearchTool, LiteLLMModel


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    web_researcher = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        max_steps=3,
    )

    managed_researcher = ManagedAgent(
        agent=web_researcher,
        name="web_researcher",
        description="Searches the web for information. Use for finding current data and facts.",
    )

    manager = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[managed_researcher],
        max_steps=5,
    )

    result = manager.run(
        "Research the top 3 AI agent frameworks in 2026 and summarize their key features."
    )

    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
