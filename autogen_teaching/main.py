# imports
from typing import Annotated
import autogen

# define the tasks
task1 = """
    Find arxiv papers that show how are people studying trust calibration in AI based systems
"""
task2 = """
    Analyze the above the results to list the application domains studied by these papers.
"""
task3 = """
    Use this data to generate a bar chart of domains and number of papers in that domain and save to a file
"""
task4 = """
    Reflect on the sequence and create a recipe containing all the steps
    necessary and name for it. Suggest well-documented, generalized python function(s)
    to perform similar tasks for coding steps in future. Make sure coding steps and
    non-coding steps are never mixed in one function. In the docstr of the function(s),
    clarify what non-coding steps are needed to use the language skill of the assistant.
"""

# create the llm config
llm_config = {
    "timeout": 120,
    "cache_seed": 43,
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["gpt-3.5-turbo"]},
    ),
    "temperature": 0,
}

# create the agents
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False
)

assistant_create_recipe = autogen.AssistantAgent(
    name="Recipe Assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "teaching",
        "use_docker": False
    }
)


# create a simple function
@user.register_for_execution()
@assistant_create_recipe.register_for_llm(description="Recipe Assistant.")
def save_recipe(recipe: Annotated[str, "Save the Recipe"]) -> str:
    with open('new_recipe.txt', 'w') as file:
        file.write(recipe)
    return recipe


# initiate the chats
user.initiate_chat(assistant, message=task1)
user.initiate_chat(assistant, message=task2, clear_history=False)
user.initiate_chat(assistant, message=task3, clear_history=False)
user.initiate_chat(assistant_create_recipe, message=task4, clear_history=False)

# initiate chat with the recipe from the file
# with open('./new_recipe.txt', 'r') as file:
#     file_content = file.read()
#
# user.initiate_chat(assistant, message=file_content)








