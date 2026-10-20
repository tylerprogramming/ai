import asyncio
from typing import Annotated

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

model_client = OpenAIChatCompletionClient(
    model="gpt-5.4-mini",
    # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
    model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
)
assistant_client = OpenAIChatCompletionClient(
    model="gpt-5.4-mini",
    # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
    model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    temperature=0,
    timeout=300,
)

planner = AssistantAgent(
    name="planner",
    model_client=model_client,
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant "
                   "to accomplish a task. Do not suggest concrete code. For any action beyond writing code or "
                   "reasoning, convert it to a step that can be implemented by writing code. For example, "
                   "browsing the web can be implemented by writing code that reads and prints the content of a web "
                   "page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If "
                   "the execution is wrong, analyze the error and suggest a fix."
)


# The assistant's tool: it asks the planner agent for a plan (a nested chat inside a tool call)
async def ask_planner(message: Annotated[str, "The response from the LLM"]) -> str:
    """Get the first 10 characters of the message"""
    result = await planner.run(task=message)
    # return the last message received from the planner
    last_message = result.messages[-1].content
    print("About to just get the first 10 characters of the message!")
    print("Here is where you can do something with the message that we received.")
    print(last_message[:10])
    return last_message


# create an AssistantAgent instance named "assistant"
# (the system message is a short version of AutoGen 0.2's default assistant prompt, which wrote code for the user to run)
assistant = AssistantAgent(
    name="assistant",
    model_client=assistant_client,
    tools=[ask_planner],
    reflect_on_tool_use=True,
    system_message="You are a helpful AI assistant. Solve tasks using your coding and language skills. When you "
                   "need to collect info or do something, suggest python or shell code in a code block for the "
                   "user to execute, and check the execution result it returns. Reply TERMINATE in the end when "
                   "everything is done.",
)

# @assistant2 tool example from the original (left disabled):
# def do_something(message: Annotated[str, "The response from the LLM"]) -> str:
#     """Do something"""
#     return "Hello there"
# assistant2 = AssistantAgent(name="assistant2", model_client=assistant_client, tools=[do_something])


async def main():
    # runs the code blocks the assistant writes, saving them into the "planning" folder
    user_proxy = CodeExecutorAgent(
        "user_proxy",
        code_executor=LocalCommandLineCodeExecutor(work_dir="planning"),
    )

    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
    team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)

    # the assistant receives a message from the user, which contains the task description
    task = """
            Suggest a fix to an open good first issue of flaml
            """

    # Like the old human_input_mode="TERMINATE": when the agents finish, you can
    # give feedback to continue the conversation, or type "exit" to end it.
    while True:
        await Console(team.run_stream(task=task))
        task = input("Give feedback to the agents, or type 'exit' to end: ")
        if task.strip().lower() == "exit":
            break

    await model_client.close()
    await assistant_client.close()


if __name__ == "__main__":
    asyncio.run(main())
