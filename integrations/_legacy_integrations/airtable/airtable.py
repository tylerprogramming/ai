import autogen
import os
import json
from dotenv import load_dotenv

from typing_extensions import Annotated
from pyairtable import Api

load_dotenv()

api = Api(os.getenv("API_KEY"))
base_id = os.getenv("BASE_ID")

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".env",
    model_api_key_map={"gpt-4": os.getenv("OPENAI_API_KEY")}
)

llm_config = {
    "temperature": 0,
    "config_list": config_list,
    "cache_seed": 45
}

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
)

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Create a record in Airtable.  Make sure there are no slashes in the json.")
def create_record(record: Annotated[str, "Create the Record"], table: Annotated[str, "The table to create record in"]):
    table = api.table(base_id, table)
    data = json.loads(record)
    created_record = table.create(data)
    return created_record


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Get a record structure.")
def get_record_structure(table: Annotated[str, "The table to get structure from"]):
    table = api.table(base_id, table)
    first = table.first()
    return first['fields']


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Retrieve all records and return in JSON format.")
def get_all_records(table: Annotated[str, "The table to get records from"]):
    table = api.table(base_id, table)
    all_records = table.all()
    return all_records


chat_result = user_proxy.initiate_chat(
    engineer,
    message="""
I need you to integrate with Airtable.  Wait for my next instructions.  If you are creating a record, first get the record
structure and then from that, format it into json that is needed to create a record.  The record must be in json format, meaning the
keys and values are both wrapped in double quotes, not single quotes.  You don't need back slashes in the json.  If it's a number, you also don't need
to have double quotes.

An example record to create:  {"Name": "John"}

That is an example structure to create a record.

Do not start until I give a command.
""",
)











