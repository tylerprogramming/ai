import dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

dotenv.load_dotenv()  # OPENAI_API_KEY from .env


def create_model_client():
    return OpenAIChatCompletionClient(model="gpt-5.4-mini")


# To use a local LLM (e.g. LM Studio) instead:
# def create_model_client():
#     return OpenAIChatCompletionClient(
#         model="local-model",
#         base_url=os.getenv("base_url"),  # e.g. http://localhost:1234/v1
#         api_key="NULL",
#         model_info={"vision": False, "function_calling": False, "json_output": False,
#                     "family": "unknown", "structured_output": False},
#     )
