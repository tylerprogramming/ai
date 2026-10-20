import asyncio

from autogen_ext.models.openai import OpenAIChatCompletionClient

# Same idea as the old 0.2 "get config list" helper: pair up API keys and base URLs.
# AutoGen v0.7 has no config lists, so we build one model client per (key, base URL) pair.
api_keys = ["SAMPLE_API_KEY"]
base_urls = ["http://localhost:8001"]


async def main():
    model_clients = [
        OpenAIChatCompletionClient(model="gpt-5.4-mini", api_key=api_key, base_url=base_url)
        for api_key, base_url in zip(api_keys, base_urls)
    ]

    # Print each client's config (API keys are masked)
    for client in model_clients:
        print(client.dump_component().model_dump_json(indent=2))

    for client in model_clients:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
