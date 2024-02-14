import autogen
import json

filter_criteria = {"model": ["lmstudio"]}

# this is used to retrieve the api key and model we want to use for the LLM
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict=filter_criteria
)

print(config_list)

# the assistant agent takes in the name, and then the llm_config
assistant = autogen.AssistantAgent(
    name="Assistant Agent",
    llm_config={
        "cache_seed": 44,           # the cache is saved with each seed number, if unchanged on next run, will produce same result
        "temperature": 0.7,
        "config_list": config_list  # the configuration for the LLM (openapi, lm studio, ollama, etc.)
    }
)

# an agent for the user that can execute code and provide feedback to the other agents
user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",      # 3 types, ALWAYS means we will have input every LLM call, NEVER means we never reply
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "tested_code",  # the directory the user agent will save tested code to
        "use_docker": False         # if false, won't look for docker to run code inside of, otherwise it will
    }
)

# if you ask it to save to disk first, it happens more often
message = """
Save the code to disk.

Can you write a total of 3 functions:

1. The first function takes in a string, and outputs the number of characters.
2. The second function checks a string to test if it is a palindrome.
3. The third function will take in a number, and return the square root of it.
"""

# this is how we execute our chat!
# we want to initiate a chat with an agent, ask it to do something in the message parameter
# when set "last_msg", it returns the last message of the dialog as the summary.
# when set "reflection_with_llm", it returns a summary extracted using an llm client
user.initiate_chat(
    recipient=assistant,
    message=message,
    silent=False,
    summary_prompt="Summarize takeaway from the conversation. Do not add any introductory phrases. If the intended "
                   "request is NOT properly addressed, please point it out.",
    summary_method="reflection_with_llm"
)

# this will dump the chat into a json file to look at
json.dump(user.chat_messages[assistant], open("conversations.json", "w"), indent=2)