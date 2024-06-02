import autogen

config_list = [
    {
        "model": "gpt-3.5-turbo",  # or gpt-3.5-turbo
        "api_key": "sk-proj-1111"
    }
]

user_proxy = autogen.UserProxyAgent(
    "user",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    },
    human_input_mode="TERMINATE",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
)

engineer = autogen.AssistantAgent(
    "engineer",
    llm_config={
        "config_list": config_list
    },
    system_message="You are a 10x Python Engineer.  You only code in Python.  You create excellent front-end "
                   "developer. Make sure to have # filename: <name of the file>.py as the first line after the triple tick marks. "
                   "When you are done, reply with TERMINATE.",
)

user_proxy.initiate_chat(
    engineer,
    message="""I want you to create two different python methods for me in 1 file.  1 will just generate a random 
    number, and the other will take in a number and then reverse it. """)
