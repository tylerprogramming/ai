import asyncio
import os

from dotenv import load_dotenv
from typing_extensions import Annotated
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

default_path = "backend_dir/"


# These plain functions are the Engineer's tools (type hints + docstring describe them to the LLM)
def list_dir(directory: Annotated[str, "Directory to check."]):
    """List files in chosen directory."""
    files = os.listdir(default_path + directory)
    return 0, files


def see_file(filename: Annotated[str, "Name and path of file to check."]):
    """Check the contents of a chosen file."""
    with open(default_path + filename, "r") as file:
        lines = file.readlines()
    formatted_lines = [f"{i + 1}:{line}" for i, line in enumerate(lines)]
    file_contents = "".join(formatted_lines)

    return 0, file_contents


def modify_code(
        filename: Annotated[str, "Name and path of file to change."],
        start_line: Annotated[int, "Start line number to replace with new code."],
        end_line: Annotated[int, "End line number to replace with new code."],
        new_code: Annotated[str, "New piece of code to replace old code with. Remember about providing indents."],
):
    """Replace old piece of code with new one. Proper indentation is important."""
    with open(default_path + filename, "r+") as file:
        file_contents = file.readlines()
        file_contents[start_line - 1: end_line] = [new_code + "\n"]
        file.seek(0)
        file.truncate()
        file.write("".join(file_contents))
    return 0, "Code modified"


def create_file_with_code(
        filename: Annotated[str, "Name and path of file to create."], code: Annotated[str, "Code to write in the file."]
):
    """Create a new file with code."""
    with open(default_path + filename, "w") as file:
        file.write(code)
    return 0, "File created successfully"


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini", temperature=0)

    engineer = AssistantAgent(
        name="Engineer",
        model_client=model_client,
        tools=[list_dir, see_file, modify_code, create_file_with_code],
        reflect_on_tool_use=True,  # after using a tool, the Engineer explains what it did
        max_tool_iterations=10,    # let it call several tools in a row (e.g. list files, then read them)
        system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
    )

    # You are the Admin: after every Engineer reply you type the next instruction
    user_proxy = UserProxyAgent("Admin")

    # The Engineer and Admin take turns; type "exit" as Admin to end the chat
    termination = TextMentionTermination("exit", sources=["Admin"]) | MaxMessageTermination(500)
    groupchat = RoundRobinGroupChat([engineer, user_proxy], termination_condition=termination)

    await Console(groupchat.run_stream(
        task="""
You will need to improve app in FastApi. For now, check out all the application files, try to understand it and wait for next instructions.
""",
    ))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
