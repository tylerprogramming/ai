import asyncio

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,
        work_dir="code",
    )

    model_client = OpenAIChatCompletionClient(
        model="llama3",  # replace this with the model you downloaded with ollama pull <model>
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        # model_info is required for non-OpenAI model names
        model_info={"vision": False, "function_calling": False, "json_output": False,
                    "family": "unknown", "structured_output": False},
    )
    # To use OpenAI instead (OPENAI_API_KEY in your environment):
    # model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

    assistant = AssistantAgent(
        name="Assistant",
        model_client=model_client,
        system_message=""" You are an amazing python developer.  You are especially good at creating games.  You are a 10x Engineer if you didn't know by now.

                        If you want the user to save the code in a file before executing it, put # filename:
                       <filename> inside the code block as the first line.  You are a helpful assistant.  Return
                       'TERMINATE' when the task is done.
                       """
    )

    # Runs the code blocks the assistant writes (saved into the "code" folder)
    code_executor = CodeExecutorAgent("executor", code_executor=executor)

    # Like the old human_input_mode="ALWAYS": you get a turn after every round to give feedback.
    # Type "exit" to end the chat.
    user_proxy = UserProxyAgent("user")

    termination = TextMentionTermination("TERMINATE", sources=["Assistant"]) | TextMentionTermination("exit", sources=["user"])
    team = RoundRobinGroupChat([assistant, code_executor, user_proxy], termination_condition=termination)

    try:
        # trying this out with saving html file!
        await Console(team.run_stream(
            task="""
            I want you to create the python code for the game snake.  Be thorough and make sure you implement all the
            rules for the game properly.  Only code the game, no documentation.
        """))
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
