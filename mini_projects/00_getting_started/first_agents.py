import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination
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

    # Runs the engineer's code blocks and saves the files into the "coding" folder
    executor = CodeExecutorAgent(
        "executor",
        # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
        code_executor=LocalCommandLineCodeExecutor(work_dir="coding", cleanup_temp_files=False),
    )

    engineer = AssistantAgent(
        "engineer",
        model_client=model_client,
        system_message="You are a 10x Python Engineer.  You only code in Python.  You create excellent front-end "
                       "developer. Make sure to have # filename: <name of the file>.py as the first line after the triple tick marks. "
                       "Only reply TERMINATE after you have seen the code run successfully, in its own message (never in the same message as a code block).",
    )

    # The engineer writes code, the executor runs it, until the engineer says TERMINATE
    team = RoundRobinGroupChat([engineer, executor], termination_condition=TextMentionTermination("TERMINATE"))

    await Console(team.run_stream(
        task="""I want you to create two different python methods for me in 1 file.  1 will just generate a random 
    number, and the other will take in a number and then reverse it. """))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
