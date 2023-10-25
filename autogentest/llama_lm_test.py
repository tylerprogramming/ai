from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL"
    }
]

llm_config = {
    "config_list": config_list,
    "seed": 47,
    "temperature": 0.5,
    "max_tokens": -1,
    "request_timeout": 6000
}

user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    max_consecutive_auto_reply=10,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

content_creator = AssistantAgent(
    name="content_creator",
    system_message="I am a content creator that talks about exciting technologies about AI.  I want to create exciting content for my audience that is about the latest AI technology.  I want to provide in-depth details of the latest AI white papers.",
    llm_config=llm_config,
)

script_writer = AssistantAgent(
    name="Script_Writer",
    system_message="I am a script writer for the Content Creator.  This should be an eloquently written script so the Content Creator can talk to the audience about AI.",
    llm_config=llm_config
)

researcher = AssistantAgent(
    name="Researcher",
    system_message="I am the researcher for the Content Creator and look up the latest white papers in AI.  Make sure to include the white paper Title and Year it was introduced to the Script_Writer.",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="I am the reviewer for the Content Creator, Script Writer, and Researcher once they are done and have come up with a script.  I will double check the script and provide feedback.",
    llm_config=llm_config
)

groupchat = GroupChat(
    agents=[user_proxy, content_creator, script_writer, researcher, reviewer], messages=[]
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="I need to create a YouTube Script that talks about the latest paper about gpt-4 on arxiv and its potential applications in software.")
