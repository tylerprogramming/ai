import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    # Local LLM served by LM Studio (OpenAI-compatible server on port 1234).
    # model_info is required because "local-model" isn't an OpenAI model name.
    model_client = OpenAIChatCompletionClient(
        model="local-model",
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0.5,
        timeout=6000,
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )

    content_creator = AssistantAgent(
        name="content_creator",
        system_message="I am a content creator that talks about exciting technologies about AI.  I want to create exciting content for my audience that is about the latest AI technology.  I want to provide in-depth details of the latest AI white papers.",
        model_client=model_client,
    )

    script_writer = AssistantAgent(
        name="Script_Writer",
        system_message="I am a script writer for the Content Creator.  This should be an eloquently written script so the Content Creator can talk to the audience about AI.",
        model_client=model_client,
    )

    researcher = AssistantAgent(
        name="Researcher",
        system_message="I am the researcher for the Content Creator and look up the latest white papers in AI.  Make sure to include the white paper Title and Year it was introduced to the Script_Writer.",
        model_client=model_client,
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        system_message="I am the reviewer for the Content Creator, Script Writer, and Researcher once they are done and have come up with a script.  I will double check the script and provide feedback.",
        model_client=model_client,
    )

    # The model picks who speaks next (like the old GroupChatManager).
    # The old GroupChat defaulted to max_round=10.
    team = SelectorGroupChat(
        participants=[content_creator, script_writer, researcher, reviewer],
        model_client=model_client,
        termination_condition=MaxMessageTermination(10),
    )

    await Console(team.run_stream(task="I need to create a YouTube Script that talks about the latest paper about gpt-4 on arxiv and its potential applications in software."))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
