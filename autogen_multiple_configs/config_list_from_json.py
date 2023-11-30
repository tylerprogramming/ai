import autogen

cheap_config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
        }
    }
)

costly_config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4",
        }
    }
)

# Assistant using GPT 3.5 Turbo
assistant_one = autogen.AssistantAgent(
    name="3.5-assistant",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": cheap_config_list,
        "temperature": 0,
    },
)

# Assistant using GPT 4
assistant_two = autogen.AssistantAgent(
    name="4-assistant",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": costly_config_list,
        "temperature": 0,
    },
)

print(costly_config_list)
