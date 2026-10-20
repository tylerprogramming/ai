from smolagents import CodeAgent, InferenceClientModel
from smolagents import tool
from huggingface_hub import list_models

from dotenv import load_dotenv

load_dotenv()

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads")))  # hub 1.x sorts descending; `direction` was removed
    
    return most_downloaded_model.id


agent = CodeAgent(tools=[model_download_tool], model=InferenceClientModel())
agent.run(
    "Give me the most downloaded model for text-generation on the Hugging Face Hub."
)