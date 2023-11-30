import autogen
import os
import openai
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "api_type": os.getenv("api_type"),
        "api_base": os.getenv("api_base"),
        "api_key": os.getenv("api_key")
    },
]

openai.api_key = os.getenv("api_key")
openai.api_base = os.getenv("api_base")

llm_config = {
    "config_list": config_list,
    "seed": 44,
    "request_timeout": 600,
    "temperature": 0.7
}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="NEVER"
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

use_memgpt = bool(os.getenv("use_memgpt"))

if not use_memgpt:
    print("Using AutoGen Coder")
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
    print("Using MemGPT Coder")
    coder = create_autogen_memgpt_agent(
        "MemGPT_coder",
        persona_description="I am a 10x engineer, trained in Python. I was the first engineer at Uber "
        "(which I make sure to tell everyone I work with).",
        user_description=f"You are participating in a group chat with a user ({user_proxy.name}) "
        f"and a product manager ({pm.name}).",
        interface_kwargs=interface_kwargs
    )

# Initialize the group chat between the user and two LLM agents (PM and coder)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=2)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager,
    message="Create a simple random number generator in python, that's it."
)
