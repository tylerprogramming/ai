import asyncio
import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# AutoGen v0.7 has no config lists. Each model gets its own model client instead.
# Here we keep the same idea as the old 0.2 "config list from dotenv" helper: map each model to the .env variable holding its key.
load_dotenv(".env")

model_api_key_map = {
    "gpt-5.4-mini": {"api_key_env_var": "OPENAI_API_KEY"},
    "gpt-5.4-mini-alt": {
        "api_key_env_var": "ANOTHER_API_KEY",
        "base_url": "http://someapi.com",
        # model_info is required for model names OpenAI doesn't know
        "model_info": {
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    },
}

# Only keep the models we want (like filter_dict)
filter_models = {"gpt-5.4-mini"}


async def main():
    model_clients = []
    for model, settings in model_api_key_map.items():
        if model not in filter_models:
            continue
        model_clients.append(
            OpenAIChatCompletionClient(
                model=model,
                api_key=os.getenv(settings["api_key_env_var"]),
                base_url=settings.get("base_url"),
                model_info=settings.get("model_info"),
            )
        )

    # Print each client's config (API keys are masked)
    for client in model_clients:
        print(client.dump_component().model_dump_json(indent=2))

    for client in model_clients:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
