import autogen

# config_list = autogen.config_list_from_json(
#     env_or_file="OAI_CONFIG_LIST",
#     filter_dict={
#         "model": ["gpt-4"]
#     },
# )

config_list = {
    "model": "NULL",  # not needed
    # NOTE: on versions of pyautogen < 0.2.0 use "api_base", and also uncomment "api_type"
    # "api_base": "http://localhost:1234/v1",
    # "api_type": "open_ai",
    "base_url": "http://localhost:1234/v1",  # ex. "http://127.0.0.1:5001/v1" if you are using webui, "http://localhost:1234/v1/" if you are using LM Studio
    "api_key": "NULL",  #  not needed
}

# print(config_list)

llm_config = {
    "temperature": 0,
    "timeout": 300,
    "seed": 43,
    "config_list": config_list,
    "functions": [
        {
            "name": "ask_planner",
            "description": "ask planner to: 1. get a plan for finishing a task, 2. verify the execution result of "
                           "the plan and potentially suggest new plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "question to ask planner. Make sure the question include enough context, "
                                       "such as the code and the execution result. The planner does not know the "
                                       "conversation between you and the user, unless you share the conversation "
                                       "with the planner.",
                    },
                },
                "required": ["message"],
            },
        },
    ],
}


def ask_planner(message):
    planner_user.initiate_chat(planner, message=message)
    # return the last message received from the planner
    last_message = planner_user.last_message()["content"]
    print("About to just get the first 10 characters of the message!")
    print("Here is where you can do something with the message that we received.")
    print(last_message[:10])
    return planner_user.last_message()["content"]


planner = autogen.AssistantAgent(
    name="planner",
    llm_config={
        "config_list": config_list
    },
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant "
                   "to accomplish a task. Do not suggest concrete code. For any action beyond writing code or "
                   "reasoning, convert it to a step that can be implemented by writing code. For example, "
                   "browsing the web can be implemented by writing code that reads and prints the content of a web "
                   "page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If "
                   "the execution is wrong, analyze the error and suggest a fix."
)

planner_user = autogen.UserProxyAgent(
    name="planner_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)

# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "content" in x and x["content"] is not None and x["content"].rstrip().endswith(
        "TERMINATE"),
    code_execution_config={"work_dir": "planning", "use_docker": False},
    function_map={"ask_planner": ask_planner},
)

# can also register functions to an agent this way
# user_proxy.register_function(
#     function_map={
#         "ask_planner": ask_planner
#     }
# )

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
            Suggest a fix to an open good first issue of flaml
            """,
)
