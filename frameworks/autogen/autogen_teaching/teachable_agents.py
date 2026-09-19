import autogen
from dotenv import load_dotenv
from autogen import ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability

load_dotenv()

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path="."
)

teachable_agent = ConversableAgent(
    name="teachable_agent",  # The name is flexible, but should not contain spaces to work in group chat.
    llm_config={"config_list": config_list, "timeout": 120, "cache_seed": None},  # Disable caching.
)

# Instantiate the Teachability capability. Its parameters are all optional.
teachability = Teachability(
    verbosity=0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
    reset_db=False,
    path_to_db_dir="./tmp/notebook/teachability_db",
    recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
)

# Now add the Teachability capability to the agent.
teachability.add_to_agent(teachable_agent)

# Instantiate a UserProxyAgent to represent the user. But in this notebook, all user input will be simulated.
user = UserProxyAgent(
    name="user",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=0,
    code_execution_config={
        "use_docker": False
    },
)

task = """
    Here is some information about me:
    
    1. My favorite programming language is Java
    2. My hobbies include AI, Drinking, and Futbol
    3. My birthday is March 3rd
"""

task_tweet = """
    Create an engaging tweet about Java
"""

task_check = """
    What day is my birthday?
"""


user.initiate_chat(
    teachable_agent,
    message=task_tweet,
    clear_history=False
)



