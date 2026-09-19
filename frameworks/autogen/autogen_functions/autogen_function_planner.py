import autogen
from typing import Annotated

config_list = autogen.config_list_from_json(
    env_or_file="config/OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-3.5-turbo"]
    },
)

llm_config = {
    "temperature": 0,
    "timeout": 300,
    "seed": 44,
    "config_list": config_list
}

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
    code_execution_config={"work_dir": "planning", "use_docker": False},
)

# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

# create an AssistantAgent instance named "assistant"
assistant2 = autogen.AssistantAgent(
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
)


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Get the first 10 characters of the message")
def ask_planner(message: Annotated[str, "The response from the LLM"]) -> str:
    planner_user.initiate_chat(planner, message=message)
    # return the last message received from the planner
    last_message = planner_user.last_message()["content"]
    print("About to just get the first 10 characters of the message!")
    print("Here is where you can do something with the message that we received.")
    print(last_message[:10])
    return planner_user.last_message()["content"]


# @user_proxy.register_for_execution()
# @assistant2.register_for_llm(description="Do something")
# def do_something(message: Annotated[str, "The response from the LLM"]) -> str:
#     return "Hello there"


# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
            Suggest a fix to an open good first issue of flaml
            """,
)
