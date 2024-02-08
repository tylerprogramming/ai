import autogen
import config

script_maker = autogen.AssistantAgent(
    name="script_maker",
    system_message="You are to create a youtube script organized with a title given a topic and only write the "
                   "script, do not write the description.",
    llm_config=config.llm_config,
)

description_maker = autogen.AssistantAgent(
    name="description_maker",
    system_message="You are to create the description for the youtube script organized and use emojis.  Only write "
                   "the description, not the script.",
    llm_config=config.llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)

group_chat = autogen.GroupChat(agents=[user_proxy, script_maker, description_maker], messages=[], max_round=5)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=config.llm_config)
