from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

# The smolagents 1.26 default (Qwen3-Next-80B-A3B-Thinking) is not served by Inference Providers; see README
HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=InferenceClientModel(model_id=HF_MODEL_ID))

agent.run("How long would it take for an elephant to cross the united states from florida to california?")
