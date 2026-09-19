import os

config_list = [
    {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": os.getenv("MODEL"),
        "base_url": os.getenv("BASE_URL")
    }
]

# set autogen user agent and assistant agent with function calling
llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}