import os

import dotenv

dotenv.load_dotenv()

config_list_openai_autogen = [
    {
        "model": os.getenv("model_gpt_4"),
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

llm_config_local_excel = {
    "config_list": config_list_openai_autogen,
    "seed": 42,
    "functions": [
        {
            "name": "create_csv",
            "description": "ask excel to: 1. get a plan for finishing a task, 2. save the csv formatted fitness plan "
                           "to a .csv file",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "make sure the message is in the style of a csv",
                    },
                },
                "required": ["message"],
            },
        },
    ],
}

llm_config_local_documents = {
    "config_list": config_list_openai_autogen,
    "seed": 42,
    "functions": [{
        "name": "create_doc",
        "description": "ask document to: 1. get a summary of the plan, 2. save the summary formatted fitness plan "
                       "to a .txt file",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "make sure the message is in the style of a txt",
                },
            },
            "required": ["message"],
        },
    }]
}

llm_config = {
    "config_list": config_list_openai_autogen,
    "seed": 42
}


