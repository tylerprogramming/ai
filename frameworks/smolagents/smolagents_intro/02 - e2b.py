from smolagents import CodeAgent, VisitWebpageTool, InferenceClientModel

from dotenv import load_dotenv

load_dotenv()

agent = CodeAgent(
    tools = [VisitWebpageTool()],
    model=InferenceClientModel(),
    additional_authorized_imports=["requests", "markdownify"],
    executor_type="e2b",  # was use_e2b_executor=True; needs E2B_API_KEY
)

agent.run("What was Abraham Lincoln's preferred pet?")