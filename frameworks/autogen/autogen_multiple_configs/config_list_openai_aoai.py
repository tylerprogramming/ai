import asyncio
from pathlib import Path

from autogen_ext.models.openai import OpenAIChatCompletionClient

# Same idea as the old 0.2 "config list for OpenAI / Azure OpenAI" helper: read the API key and base URL from text files in the txt folder.
# AutoGen v0.7 has no config lists, so we build a model client from them directly.
TXT_DIR = Path("txt")


def read_txt(name: str) -> str:
    return (TXT_DIR / name).read_text().strip()


async def main():
    # OpenAI-compatible endpoint (key_openai.txt + base_openai.txt)
    openai_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        api_key=read_txt("key_openai.txt"),
        base_url=read_txt("base_openai.txt"),
    )

    # Azure OpenAI is excluded here (exclude='aoai'). To use it, build an Azure client instead:
    # from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    # aoai_client = AzureOpenAIChatCompletionClient(
    #     model="gpt-5.4-mini",
    #     azure_deployment="your-deployment-name",
    #     api_version="2024-06-01",
    #     api_key=read_txt("key_aoai.txt"),
    #     azure_endpoint=read_txt("base_aoai.txt"),
    # )

    # Print the client's config (the API key is masked)
    print(openai_client.dump_component().model_dump_json(indent=2))

    await openai_client.close()


if __name__ == "__main__":
    asyncio.run(main())
