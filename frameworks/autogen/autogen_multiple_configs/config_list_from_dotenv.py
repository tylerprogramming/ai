import autogen

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env',
    model_api_key_map={
        "gpt-5.4-mini": "OPENAI_API_KEY",
        "gpt-5.4-mini-alt": {
            "api_key_env_var": "ANOTHER_API_KEY",
            "api_type": "openai",
            "api_version": "v4",
            "api_base": "http://someapi.com"
        }
    },
    filter_dict={
        "model": {
            "gpt-5.4-mini"
        }
    }
)

print(config_list)
