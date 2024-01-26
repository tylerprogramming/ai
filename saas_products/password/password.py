import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

llm_config = {
    "config_list": config_list,
    "seed": 42,
    "temperature": 0.7,
    "timeout": 300
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved "
                   "by this admin.",
    human_input_mode="TERMINATE",
    code_execution_config={"last_n_messages": 3, "work_dir": "programming", "use_docker": False},
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin 
    approval. The plan may involve an engineer who can write code and an executor and critic who doesn't write code. 
    Explain the plan first. Be clear which step is performed by an engineer, executor, and critic.''',
    llm_config=llm_config,
)

executor = autogen.AssistantAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.  Once you execute the "
                   "code, save it into a proper file under the correct directory.",
    llm_config=llm_config
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback.  You don't "
                   "execute code, just provide feedback.",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, engineer, planner, executor, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="I would like to build a simple application that allows me to call an api "
                                          "to encrypt a message, which will be in the form of a string, and use the "
                                          "RSA encryption algorithm.  Then this encrypted message should be stored in "
                                          "a database table called Messages, which takes an id and then the column "
                                          "for the message.  There should be another API that can be called to "
                                          "retrieve the message based on an id, then grab the associated encrypted "
                                          "message, decrypt it also using RSA and return the decrypted message.  Can "
                                          "you create this as a flask application?")
