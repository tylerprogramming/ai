from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat


def create_team(model_client):
    script_maker = AssistantAgent(
        name="script_maker",
        system_message="You are to create a youtube script organized with a title given a topic and only write the "
                       "script, do not write the description.",
        model_client=model_client,
    )

    description_maker = AssistantAgent(
        name="description_maker",
        system_message="You are to create the description for the youtube script organized and use emojis.  Only write "
                       "the description, not the script.",
        model_client=model_client,
    )

    # The model picks who speaks next (like the old GroupChatManager); max_round=5 -> 5 messages.
    # The old user_proxy only started the chat, so the request is now passed as the team's task.
    return SelectorGroupChat(
        [script_maker, description_maker],
        model_client=model_client,
        termination_condition=MaxMessageTermination(5),
    )
