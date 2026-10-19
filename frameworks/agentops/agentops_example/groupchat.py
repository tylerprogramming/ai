import asyncio
import os

import agentops
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY and AGENTOPS_API_KEY from .env

# Start recording this run in AgentOps
agentops.init(os.getenv("AGENTOPS_API_KEY"))


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    # Runs the code blocks the engineer writes and saves them into the "code" folder
    executor = CodeExecutorAgent(
        "executor",
        code_executor=LocalCommandLineCodeExecutor(
            timeout=10,  # Timeout for each code execution in seconds.
            work_dir="code"  # the directory
        ),
    )

    planner = AssistantAgent(
        "planner",
        model_client=model_client,
        system_message="You are a planner.  When you get the message, your job is to come up with a plan.  "
                       "When you are done, reply with TERMINATE"
    )

    engineer = AssistantAgent(
        "engineer",
        model_client=model_client,
        system_message="You are a 10x Python Engineer.  You only code in Python.  You create excellent front-end "
                       "developer.  When you are done, reply with "
                       "TERMINATE.  Make sure to have # <name of the file>.py after the ``` on each piece of code.",
    )

    critic = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="Your job is to critique the plan and code, and modify anything if necessary.  If it looks good "
                       "then just let it be.  When you are done, reply with TERMINATE",
    )

    # The model picks who speaks next (like the old GroupChatManager)
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(15)
    group_chat = SelectorGroupChat(
        [planner, engineer, critic, executor],
        model_client=model_client,
        termination_condition=termination,
    )

    task = """
        I want you to come up with a plan on how we would create a full front end with:

        1. multiple html pages
        2. routing to each page and from each page
        3. style with bootstrap
        4. have a button on each page that performs a function that will give a random number when clicked

        Save all of these in the necessary files.  The first line of each file should have # <filename> and the extension of the file, i.e. 
        index.html, index.js, etc.  
    """

    # Like the old human_input_mode="TERMINATE": when the agents finish, you can
    # give feedback to continue the conversation, or type "exit" to end it.
    while True:
        await Console(group_chat.run_stream(task=task))
        task = input("Give feedback to the agents, or type 'exit' to end: ")
        if task.strip().lower() == "exit":
            break

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
    agentops.end_session("Success")
