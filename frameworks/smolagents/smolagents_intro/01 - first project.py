from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=InferenceClientModel())

agent.run("How long would it take for an elephant to cross the united states from florida to california?")
