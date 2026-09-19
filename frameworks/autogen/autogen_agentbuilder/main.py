import json
import utility
import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

config_file_or_env = "OAI_CONFIG_LIST"
llm_config = {
    "temperature": 0.7
}
config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={
    "model": ["gpt-4"]
})

position_list = utility.position_list
agent_prompt = utility.agent_sys_msg_prompt
library_path_or_json = "./agents.json"

build_manager = autogen.OpenAIWrapper(config_list=config_list)
sys_msg_list = []


def generate_agents():
    for pos in position_list:
        resp_agent_sys_msg = (
            build_manager.create(
                messages=[
                    {
                        "role": "user",
                        "content": agent_prompt.format(
                            position=pos,
                            default_sys_msg=autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE
                        )
                    }
                ]
            )
            .choices[0]
            .message
            .content
        )

        sys_msg_list.append(
            {
                "name": pos,
                "profile": resp_agent_sys_msg
            }
        )


def start_task(execution_task: str, agent_list: list):
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)


generate_agents()
json.dump(sys_msg_list, open(library_path_or_json, "w"), indent=4)

new_builder = AgentBuilder(
    config_file_or_env=config_file_or_env,
    builder_model="gpt-4",
    agent_model="gpt-4",
)

agent_list, _ = new_builder.build_from_library(utility.building_task, library_path_or_json, llm_config)
saved_path = new_builder.save("./autogen_ab")

start_task(
    execution_task=utility.execution_task,
    agent_list=agent_list,
)

new_builder.clear_all_agents()
