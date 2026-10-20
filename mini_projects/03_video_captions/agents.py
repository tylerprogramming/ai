from autogen_agentchat.agents import AssistantAgent

import functions
import config


def create_chatbot(model_client):
    # The chatbot calls the transcribe/caption function itself (it's registered as a tool),
    # so there's no separate user_proxy to execute functions anymore.
    return AssistantAgent(
        name="chatbot",
        system_message=f"You are in charge of taking a video file and then caption it after"
                       f"transcribing it.",
        model_client=model_client,
        tools=[functions.recognize_transcript_from_video],
        reflect_on_tool_use=True,  # explain the tool result instead of returning raw output
    )


async def caption_video(task):
    """Run the chatbot on a task like 'Caption the video uploads/my.mp4 and name it my_captioned'."""
    model_client = config.create_model_client()
    try:
        result = await create_chatbot(model_client).run(task=task)
    finally:
        await model_client.close()
    return result.messages[-1].to_text()
