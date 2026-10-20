import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    )

    # Create a local command line code executor.
    # Code blocks that start with "# filename: <filename>" are saved under that name in the "code" folder.
    # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
    executor = LocalCommandLineCodeExecutor(
        timeout=10,
        work_dir="code",
        cleanup_temp_files=False,
    )

    assistant = AssistantAgent(
        name="Assistant",
        model_client=model_client,
        system_message="If you want the user to save the code in a file before executing it, put # filename: "
                       "<filename> inside the code block as the first line.  Only python and sh code blocks are "
                       "executed, so save HTML, CSS and JavaScript files by writing them from a python script.  "
                       "You are a helpful assistant.  Return 'TERMINATE' when the task is done."
    )

    # The user agent runs the code blocks the assistant writes
    user_proxy = CodeExecutorAgent("user", code_executor=executor)

    # Stop when the assistant says TERMINATE, or after 20 messages as a safety net
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
    team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)

    # trying this out with saving html file!
    try:
        await Console(team.run_stream(task="""
        Create a simple html that opens a simple home page and stylize it
        with some css and save that in a separate file.  Create a simple
        button on the html page that when clicked, just displays 'Hello!'.
        You can also create a javascript file to make this happen.
        Make sure to comment out the file names at the top of each file.
        """))
    finally:
        await executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
