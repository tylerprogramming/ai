import dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

dotenv.load_dotenv()  # OPENAI_API_KEY from .env


def create_model_client():
    return OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )


# To use a local LLM (e.g. LM Studio) instead:
# def create_model_client():
#     return OpenAIChatCompletionClient(
#         model="local-model",
#         base_url=os.getenv("base_url"),  # e.g. http://localhost:1234/v1
#         api_key="NULL",
#         model_info={"vision": False, "function_calling": True, "json_output": False,
#                     "family": "unknown", "structured_output": False},
#     )

# The old llm_config["functions"] schema is gone: in AutoGen v0.7 the tool schema is built
# from the type hints and docstring of functions.recognize_transcript_from_video.
