import autogen
import system
import config
import functions

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="TERMINATE",
)

# The agent playing the role of the product manager (PM)
pm = autogen.AssistantAgent(
    name=system_messages.product_manager_name,
    system_message=system_messages.product_manager,
    llm_config=config.llm_config,
)

fitness_expert = autogen.AssistantAgent(
    name=system_messages.fitness_expert_name,
    system_message=system_messages.fitness_expert,
    llm_config=config.llm_config_local_excel,
)

doc_expert = autogen.AssistantAgent(
    name=system_messages.document_expert_name,
    llm_config=config.llm_config_local_documents,
    system_message=system_messages.document_expert
)

csv_user = autogen.UserProxyAgent(
    name="csv_user",
    max_consecutive_auto_reply=0,
    system_message="You Don't write any code, instead just make sure the message is in csv format and if it's not, "
                   "ensure that it is.  Then save the file to workout.csv",
    human_input_mode="NEVER",
)

doc_user = autogen.UserProxyAgent(
    name="doc_user",
    max_consecutive_auto_reply=0,
    system_message="You Don't write any code, instead just make sure the message is a summary and if it's not, "
                   "ensure that it is.  Then save the file to workout.txt",
    human_input_mode="NEVER",
)

excel = autogen.AssistantAgent(
    name=system_messages.excel_expert_name,
    llm_config=config.llm_config,
    system_message=system_messages.excel_expert,
)

document = autogen.AssistantAgent(
    name=system_messages.document_expert_name,
    llm_config=config.llm_config,
    system_message=system_messages.document_expert,
)

group_chat = autogen.GroupChat(agents=[user_proxy, pm, fitness_expert, doc_expert], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=config.llm_config)

fitness_expert.register_function(
    function_map={
        "create_csv": functions.create_csv
    }
)

doc_expert.register_function(
    function_map={
        "create_doc": functions.create_doc,
    }
)