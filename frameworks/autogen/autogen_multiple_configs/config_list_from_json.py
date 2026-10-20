import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env


async def main():
    # AutoGen v0.7 replaces config lists (a JSON file of models + filter_dict) with one model client per model.
    # Swap in a cheaper or more capable model name for each client.
    cheap_model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # GPT-5 models only accept the default temperature (and max_completion_tokens, not max_tokens), so the old GPT-4 sampling settings were dropped
        timeout=600,
    )
    costly_model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # GPT-5 models only accept the default temperature (and max_completion_tokens, not max_tokens), so the old GPT-4 sampling settings were dropped
        timeout=600,
    )

    # Assistant using the cheap model
    assistant_one = AssistantAgent(
        name="cheap_assistant",
        model_client=cheap_model_client,
    )

    # Assistant using the costly model
    assistant_two = AssistantAgent(
        name="costly_assistant",
        model_client=costly_model_client,
    )

    print(assistant_one.name, "and", assistant_two.name, "are ready.")

    # Print the costly client's config (the API key is masked)
    print(costly_model_client.dump_component().model_dump_json(indent=2))

    await cheap_model_client.close()
    await costly_model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
