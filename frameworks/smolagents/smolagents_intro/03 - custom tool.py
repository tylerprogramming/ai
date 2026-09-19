from smolagents import CodeAgent, HfApiModel
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
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    
    return most_downloaded_model.id


agent = CodeAgent(tools=[model_download_tool], model=HfApiModel())
agent.run(
    "Give me the most downloaded model for text-generation on the Hugging Face Hub."
)