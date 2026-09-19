import autogen

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env',
    model_api_key_map={
        "gpt-4": "OPENAI_API_KEY",
        "gpt-3.5-turbo": {
            "api_key_env_var": "ANOTHER_API_KEY",
            "api_type": "openai",
            "api_version": "v4",
            "api_base": "http://someapi.com"
        }
    },
    filter_dict={
        "model": {
            "gpt-3.5-turbo"
        }
    }
)

print(config_list)
