import autogen

from typing_extensions import Annotated
from pyairtable import Api

api = Api("patDZtaAICj2lkALu.3aa39b55e9531f03650e51bed4e56a30ffbc65775e17ca6c08387581fd58eb16")
base_id = "appRcimSdzB4syDWp"

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
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
@engineer.register_for_llm(description="Create a record in Airtable.  Make sure there are no back slashes in the json.")
def create_record(record: Annotated[str, "Create the Record"], table: Annotated[str, "The table to create record in"]):
    table = api.table(base_id, table)
    created_record = table.create(record)
    return created_record


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Get a record structure.")
def get_record_structure(table: Annotated[str, "The table to get structure from"]):
    table = api.table(base_id, table)
    first = table.first()
    return first['fields']


chat_result = user_proxy.initiate_chat(
    engineer,
    message="""
I need you to integrate with Airtable.  Wait for my next instructions.  If you are creating a record, first get the record
structure and then from that, format it into json that is needed to create a record.  The record must be in json format, meaning the 
keys and values are both wrapped in double quotes, not single quotes.  You don't need back slashes in the json.  If it's a number, you also don't need 
to have double quotes.
""",
)
