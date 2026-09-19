from smolagents import CodeAgent, VisitWebpageTool, HfApiModel

from dotenv import load_dotenv

load_dotenv()

agent = CodeAgent(
    tools = [VisitWebpageTool()],
    model=HfApiModel(),
    additional_authorized_imports=["requests", "markdownify"],
    use_e2b_executor=True
)

agent.run("What was Abraham Lincoln's preferred pet?")