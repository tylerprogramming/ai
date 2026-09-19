import os
import dotenv

dotenv.load_dotenv()

# config_list = [
#     {
#         "model": os.getenv("model_gpt_4"),
#         "api_key": os.getenv("OPENAI_API_KEY"),
#     }
# ]

config_list = [
    {
        "model": "NULL",
        "base_url": os.getenv("base_url"),
        "api_key": "NULL",
    },
]

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}
