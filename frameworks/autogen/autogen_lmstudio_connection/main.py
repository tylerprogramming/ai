import autogen


def main():
    config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

    # Create the agent that uses the LLM.
    assistant = autogen.AssistantAgent("assistant", llm_config={"config_list": config_list})

    # Create the agent that represents the user in the conversation.
    user_proxy = autogen.UserProxyAgent("user_proxy",
                                        code_execution_config={"work_dir": "coding", "use_docker": False})

    user_proxy.initiate_chat(assistant, message="Generate a function that acts like the 8 Ball with random phrases.")


if __name__ == "__main__":
    main()
