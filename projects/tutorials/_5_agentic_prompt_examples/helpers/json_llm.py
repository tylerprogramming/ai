import json
from pydantic import ValidationError, BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def JSON_llm(user_prompt: str, schema: BaseModel, system_prompt: str = None):
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
    
        messages.append({"role": "user", "content": user_prompt})
        
        # Define the JSON schema based on the Pydantic model
        json_schema = schema.model_json_schema()

        extract = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": json_schema
                }
            },
        )
        return json.loads(extract.choices[0].message.content)

    except ValidationError as e:
        error_message = f"Failed to parse JSON: {e}"
        print(error_message)