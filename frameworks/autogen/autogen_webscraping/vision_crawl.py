import asyncio
import subprocess
import os
from pathlib import Path

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env


def create_screenshot(url, user_response_ss_name):
    """Use puppeteer (screenshot.js) to take a full-page screenshot of the url."""
    print(f"Crawling {url}")

    if os.path.exists(user_response_ss_name):
        os.remove(user_response_ss_name)

    result = subprocess.run(
        ["node", "screenshot.js", url, user_response_ss_name],
        capture_output=True,
        text=True
    )

    exitcode = result.returncode

    if not exitcode == 0:
        print(f"Error with exitcode {exitcode} : {result.stderr}")
        return "ERROR"

    return user_response_ss_name


async def initiate_chat():
    user_response_url = input("What is the url you want to check?:")
    user_response_message = input("What do you want from this url?:")
    user_response_ss_name = input("What name do you want to give the screenshot?:")

    screenshot = create_screenshot(user_response_url, user_response_ss_name)

    if screenshot == "ERROR":
        return "I was unable to crawl that site, check error and try again."

    print("Image captured")

    # gpt-5.4-mini supports vision, so a normal AssistantAgent can look at images
    # (this replaces the old MultimodalConversableAgent)
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # GPT-5 models only accept the default temperature (and max_completion_tokens, not max_tokens), so the old GPT-4 sampling settings were dropped
    )

    image_agent = AssistantAgent(
        name="image_explainer",
        model_client=model_client,
    )

    # Example 1 - publix
    # The image is sent as part of a MultiModalMessage (instead of an <img ...> tag)
    message = MultiModalMessage(
        content=[
            f"What is this a picture of?\n\n{user_response_message}",
            Image.from_file(Path(screenshot)),
        ],
        source="user",
    )
    await Console(image_agent.run_stream(task=message))

    # Example 2
    # message = MultiModalMessage(
    #     content=[
    #         "What is this a picture of?\n\n"
    #         "Can you give me a list of all the items and their prices from this image from amazon?.",
    #         Image.from_file(Path("screenshot.jpg")),
    #     ],
    #     source="user",
    # )
    # await Console(image_agent.run_stream(task=message))

    await model_client.close()


if __name__ == "__main__":
    response = asyncio.run(initiate_chat())
    if response:
        print(response)
