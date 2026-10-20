import asyncio
import json
import os

from dotenv import load_dotenv
from typing_extensions import Annotated
from pyairtable import Api

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY, API_KEY (Airtable) and BASE_ID from .env

api = Api(os.getenv("API_KEY"))
base_id = os.getenv("BASE_ID")


# Tools: plain Python functions with type hints + docstrings. The docstring is the tool description.
def create_record(record: Annotated[str, "Create the Record"], table: Annotated[str, "The table to create record in"]) -> dict:
    """Create a record in Airtable.  Make sure there are no slashes in the json."""
    table = api.table(base_id, table)
    data = json.loads(record)
    created_record = table.create(data)
    return created_record


def get_record_structure(table: Annotated[str, "The table to get structure from"]) -> dict:
    """Get a record structure."""
    table = api.table(base_id, table)
    first = table.first()
    return first['fields']


def get_all_records(table: Annotated[str, "The table to get records from"]) -> list:
    """Retrieve all records and return in JSON format."""
    table = api.table(base_id, table)
    all_records = table.all()
    return all_records


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # temperature=0 removed: gpt-5 models only accept the default temperature
    )

    engineer = AssistantAgent(
        name="Engineer",
        model_client=model_client,
        tools=[create_record, get_record_structure, get_all_records],
        reflect_on_tool_use=True,
        system_message="""
        I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
        """,
    )

    # The human (you) types instructions in the terminal. Type "exit" to end the chat.
    user_proxy = UserProxyAgent(name="Admin")

    team = RoundRobinGroupChat(
        [engineer, user_proxy],
        termination_condition=TextMentionTermination("exit", sources=["Admin"]),
    )

    await Console(team.run_stream(task="""
I need you to integrate with Airtable.  Wait for my next instructions.  If you are creating a record, first get the record
structure and then from that, format it into json that is needed to create a record.  The record must be in json format, meaning the
keys and values are both wrapped in double quotes, not single quotes.  You don't need back slashes in the json.  If it's a number, you also don't need
to have double quotes.

An example record to create:  {"Name": "John"}

That is an example structure to create a record.

Do not start until I give a command.
"""))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
