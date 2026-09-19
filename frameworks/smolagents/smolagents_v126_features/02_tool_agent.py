"""
Smolagents Tool Agent Example

An agent that uses tools without writing code.
"""

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    agent = ToolCallingAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        max_steps=3,
    )

    result = agent.run("What are the latest developments in AI agents for 2026?")

    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
