"""
Smolagents Code Agent Example

An agent that writes and executes Python code to solve problems.
"""

from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        max_steps=5,
    )

    result = agent.run(
        "What is the population of Tokyo and New York combined? "
        "Search for the current populations and calculate the sum."
    )

    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
