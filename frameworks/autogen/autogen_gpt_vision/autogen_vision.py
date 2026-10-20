import asyncio
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image as PILImage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

image_goldendoodle = "https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0"
image_corgi = "https://cdn.pixabay.com/photo/2019/08/19/07/45/corgi-4415649_1280.jpg"
image_luigi_yoshi_mario = "https://cdn.pixabay.com/photo/2016/07/30/14/25/mario-1557240_1280.jpg"
image_super_nintendo = "https://cdn.pixabay.com/photo/2018/04/26/06/59/technology-3351286_1280.jpg"
image_mitochondria = "https://cdn.pixabay.com/photo/2021/07/18/05/36/cell-6474673_1280.jpg"
image_waldo = "https://i.stack.imgur.com/reNlF.jpg"


def image_from_url(url: str) -> Image:
    """Download an image so it can be sent to the agent (replaces the old <img url> tags)."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return Image.from_pil(PILImage.open(BytesIO(response.content)))


async def main():
    # gpt-5.4-mini supports vision, so a normal AssistantAgent can look at images
    # (this replaces the old MultimodalConversableAgent)
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        temperature=0.5,
        max_tokens=500,
    )

    image_agent = AssistantAgent(
        name="image_explainer",
        model_client=model_client,
    )

    # Example 1
    await Console(image_agent.run_stream(task=MultiModalMessage(
        content=["Can you please find waldo in this image?", image_from_url(image_waldo)],
        source="user",
    )))

    # Example 2
    # (calling run_stream again on the same agent continues the conversation, like the old user_proxy.send)
    # await Console(image_agent.run_stream(task=MultiModalMessage(
    #     content=["What is this picture of and describe everything in it?", image_from_url(image_goldendoodle)],
    #     source="user",
    # )))
    #
    # await Console(image_agent.run_stream(task=MultiModalMessage(
    #     content=[
    #         "What dog is this a picture of?",
    #         image_from_url(image_corgi),
    #         "Which of these dogs tends to bark more, this one or the previous dog image?",
    #     ],
    #     source="user",
    # )))

    # Example 3
    # await Console(image_agent.run_stream(task=MultiModalMessage(
    #     content=["What is this picture of and describe everything in it?", image_from_url(image_luigi_yoshi_mario)],
    #     source="user",
    # )))
    #
    # await Console(image_agent.run_stream(task=MultiModalMessage(
    #     content=[
    #         "What game is displayed here?",
    #         image_from_url(image_super_nintendo),
    #         "Among all of these characters, which one has sold the most amount of games?  Can you also give some "
    #         "figures for all characters shown?",
    #     ],
    #     source="user",
    # )))

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
