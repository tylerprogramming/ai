import asyncio

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    # Connect to the local LM Studio server (start it in LM Studio's "Local Server" tab).
    # LM Studio speaks the OpenAI API, so we use the OpenAI client with a custom base_url.
    # model_info is required because "phi" isn't an OpenAI model name.
    model_client = OpenAIChatCompletionClient(
        model="phi",
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )

    # Create the agent that uses the LLM.
    assistant = AssistantAgent(
        "assistant",
        model_client=model_client,
        system_message="You are a helpful AI assistant. Solve tasks by writing Python code in markdown "
                       "code blocks. When the task is done, reply with TERMINATE.",
    )

    # Create the agent that runs the code the assistant writes (in the "coding" folder).
    code_executor = LocalCommandLineCodeExecutor(work_dir="coding")
    executor = CodeExecutorAgent("executor", code_executor=code_executor)

    # Stop when the assistant says TERMINATE, or after 20 messages as a safety net.
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
    team = RoundRobinGroupChat([assistant, executor], termination_condition=termination)

    try:
        await Console(team.run_stream(task="Generate a function that acts like the 8 Ball with random phrases."))
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
