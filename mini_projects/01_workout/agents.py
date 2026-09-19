import autogen
import config
import system_messages

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message=system_messages.user_proxy_message,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config= {
        "work_dir": "code",
        "use_docker": False
    }
)

fitness_expert = autogen.AssistantAgent(
    name=system_messages.fitness_expert_name,
    system_message=system_messages.fitness_expert_message,
    llm_config=config.llm_config,
)