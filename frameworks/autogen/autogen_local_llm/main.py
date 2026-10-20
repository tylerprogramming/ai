import asyncio

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from CustomModelClient import CustomModelClient


async def main():
    # Our own model client that runs a HuggingFace model locally (see CustomModelClient.py).
    model_client = CustomModelClient(model="stabilityai/stable-code-3b", device="cpu", max_length=1000)

    assistant = AssistantAgent(
        "assistant",
        model_client=model_client,
        system_message="You are a helpful AI assistant. Solve tasks by writing Python code in markdown "
                       "code blocks. When the task is done, reply with TERMINATE.",
    )

    # Runs the code the assistant writes, in the "coding" folder.
    # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
    code_executor = LocalCommandLineCodeExecutor(work_dir="coding", cleanup_temp_files=False)
    executor = CodeExecutorAgent("executor", code_executor=code_executor)

    # Small local models don't always say TERMINATE, so also cap the number of messages.
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
    team = RoundRobinGroupChat([assistant, executor], termination_condition=termination)

    try:
        await Console(team.run_stream(task="Write python code to print Hello World!"))
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
