from smolagents import CodeAgent, VisitWebpageTool, InferenceClientModel

from dotenv import load_dotenv

# The smolagents 1.26 default (Qwen3-Next-80B-A3B-Thinking) is not served by Inference Providers; see README
HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"

load_dotenv()

agent = CodeAgent(
    tools = [VisitWebpageTool()],
    model=InferenceClientModel(model_id=HF_MODEL_ID),
    additional_authorized_imports=["requests", "markdownify"],
    executor_type="e2b",  # was use_e2b_executor=True; needs E2B_API_KEY
)

agent.run("What was Abraham Lincoln's preferred pet?")