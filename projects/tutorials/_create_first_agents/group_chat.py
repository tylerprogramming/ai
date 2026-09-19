import autogen
from autogen.coding import LocalCommandLineCodeExecutor

config_list = [
    {
        "model": "gpt-4",
        "api_key": "sk-proj-1111"
    }
]

executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir="code"  # the directory
)

user_proxy = autogen.UserProxyAgent(
    "user",
    code_execution_config={"executor": executor},
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

planner = autogen.AssistantAgent(
    "planner",
    llm_config={
        "config_list": config_list
    },
    system_message="You are a planner.  When you get the message, your job is to come up with a plan.  "
                   "When you are done, reply with TERMINATE"
)

engineer = autogen.AssistantAgent(
    "engineer",
    llm_config={
        "config_list": config_list
    },
    system_message="You are a 10x Python Engineer.  You only code in Python.  You create excellent front-end "
                   "developer.  When you are done, reply with "
                   "TERMINATE.  Make sure to have # <name of the file>.py after the ``` on each piece of code.",
)

critic = autogen.AssistantAgent(
    "critic",
    llm_config={
        "config_list": config_list
    },
    system_message="Your job is to critique the plan and code, and modify anything if necessary.  If it looks good "
                   "then just let it be.  When you are done, reply with TERMINATE",
)

group_chat = autogen.GroupChat(agents=[user_proxy, planner, engineer, critic], messages=[], max_round=15)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list})

user_proxy.initiate_chat(
    manager,
    message="""
        I want you to come up with a plan on how we would create a full front end with:
        
        1. multiple html pages
        2. routing to each page and from each page
        3. style with bootstrap
        4. have a button on each page that performs a function that will give a random number when clicked  
    """)
