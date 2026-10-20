import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
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

    # A short version of AutoGen 0.2's default assistant prompt: write code for the executor to run.
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful AI assistant. Solve tasks using your coding and language skills. Write "
                       "python code in a code block, with '# filename: <filename>' as the first line when the code "
                       "should be saved to a file. Only reply TERMINATE after you have seen the code run successfully, in its own message (never in the same message as a code block).",
    )

    # Runs the code blocks the assistant writes, saving files into the "code" folder
    executor = CodeExecutorAgent(
        "executor",
        # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
        code_executor=LocalCommandLineCodeExecutor(work_dir="code", cleanup_temp_files=False),
    )

    # You (the human) get a turn after each execution. Type "exit" to stop.
    user_proxy = UserProxyAgent("user_proxy")

    termination = TextMentionTermination("TERMINATE") | TextMentionTermination("exit", sources=["user_proxy"])

    team = RoundRobinGroupChat([assistant, executor, user_proxy], termination_condition=termination)

    await Console(team.run_stream(task="Write to a python file the code to plot a chart of the top 10 countries by land mass."))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
