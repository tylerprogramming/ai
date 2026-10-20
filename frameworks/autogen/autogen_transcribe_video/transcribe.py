import asyncio
from typing import Annotated

import dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import functions

dotenv.load_dotenv()  # OPENAI_API_KEY from .env


# In AutoGen v0.7, tools are plain Python functions. The type hints and docstrings
# become the tool schema the model sees (no more hand-written JSON "functions" list).
def recognize_transcript_from_video(
    audio_filepath: Annotated[str, "path of the video file"],
) -> str:
    """recognize the speech from video and transfer into a txt file"""
    return str(functions.recognize_transcript_from_video(audio_filepath))


def translate_transcript(
    source_language: Annotated[str, "source language"],
    target_language: Annotated[str, "target language"],
) -> str:
    """using translate_text function to translate the script"""
    return functions.translate_transcript(source_language, target_language)


async def initiate_chat():
    target_video = input("What is your target video path?: ")
    source_language = input("What is the source language? (i.e. English): ")
    target_language = input("What is destination language? (i.e. French): ")

    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )

    chatbot = AssistantAgent(
        name="chatbot",
        model_client=model_client,
        tools=[recognize_transcript_from_video, translate_transcript],
        reflect_on_tool_use=True,  # summarize the tool results when done
        max_tool_iterations=10,  # allow several tool calls in a row (transcribe, then translate)
        system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE "
                       "when the task is done.",
    )

    await Console(
        chatbot.run_stream(
            task=f"For the video located in {target_video}, recognize the speech and transfer it into a script "
                 f"file, then translate from {source_language} text to a {target_language} video subtitle text, "
                 f"and transfer it into a script file called transcribed.txt. ",
        )
    )
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(initiate_chat())
