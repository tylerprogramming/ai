import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4"],
    },
)

llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

initializer = autogen.UserProxyAgent(
    name="Init",
    code_execution_config=False
)

coder = autogen.AssistantAgent(
    name="coder",
    llm_config=llm_config,
    system_message="""
    Make sure to save the code to disk.
    You are the Coder. Given a topic, write code to retrieve related papers from the arXiv API, 
    print their title, authors, abstract, and link. You write python/shell code to solve tasks. Wrap the code in a 
    code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code 
    which requires others to modify. Don't use a code block if it's not intended to be executed by the executor. 
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the 
    execution result returned by the executor. If the result indicates there is an error, fix the error and output 
    the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if 
    the task is not solved even after the code is executed successfully, analyze the problem, revisit your 
    assumption, collect additional info you need, and think of a different approach to try.
    """,
)

executor = autogen.UserProxyAgent(
    name="executor",
    system_message="Executor. Execute the code written by the Coder and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False,
    },
)
scientist = autogen.AssistantAgent(
    name="scientist",
    llm_config=llm_config,
    system_message="""You are the Scientist. Please categorize papers after seeing their abstracts printed and create 
    a markdown table with Domain, Title, Authors, Summary and Link""",
)


def state_transition(last_speaker, groupchat):
    messages = groupchat.messages

    if last_speaker is initializer:
        return coder
    elif last_speaker is coder:
        return executor
    elif last_speaker is executor:
        if "exitcode: 1" in messages[-1]["content"]:
            return coder
        else:
            return scientist
    elif last_speaker is scientist:
        return None


groupchat = autogen.GroupChat(
    agents=[initializer, coder, executor, scientist],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

initializer.initiate_chat(
    manager, message="Topic: LLM applications papers from last week. Requirement: 5 - 10 papers from different domains."
)