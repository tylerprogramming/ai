import autogen
import os
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": os.getenv("model"),  # ex. This is the model name, not the wrapper
        "api_key": os.getenv("api_key")
    },
]

config_list_memgpt = [
    {
        "model": "gpt-3.5",
    },
]

llm_config = {
    "config_list": config_list,
    "seed": 42,
    "request_timeout": 600
}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE"
)

# The agent playing the role of the product manager (PM)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config
)

# Set to True if you want to print MemGPT's inner workings.
DEBUG = True

interface_kwargs = {
    "debug": DEBUG,
    "show_inner_thoughts": DEBUG,
    "show_function_outputs": DEBUG,
}

if not os.getenv("use_memgpt"):
    coder = autogen.AssistantAgent(
        name="Coder",
        system_message=f"I am a 10x engineer, trained in Python. I was the first engineer at Uber "
                       f"(which I make sure to tell everyone I work with).\n"
                       f"You are participating in a group chat with a user ({user_proxy.name}) "
                       f"and a product manager ({pm.name}).",
        llm_config=llm_config,
    )
#
else:
    coder = create_autogen_memgpt_agent(
        "MemGPT_coder",
        persona_description="I am a 10x engineer, trained in Python. I was the first engineer at Uber "
        "(which I make sure to tell everyone I work with).",
        user_description=f"You are participating in a group chat with a user ({user_proxy.name}) "
        f"and a product manager ({pm.name}).",
        model=os.getenv("model"),
        interface_kwargs=interface_kwargs
    )

# Initialize the group chat between the user and two LLM agents (PM and coder)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager,
    message="Can you make a simple flask application that has a button in the middle and generates a random number on "
            "the screen when it's clicked?"
)
