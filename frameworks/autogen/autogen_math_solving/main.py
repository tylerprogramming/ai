import asyncio

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()  # OPENAI_API_KEY from .env


async def main():
    # configuration
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini", timeout=600, seed=42)

    # AutoGen 0.2 had a dedicated MathUserProxyAgent (MathChat). In v0.7 we get the same idea
    # with an assistant that solves the problem with Python, plus an agent that runs that code.
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful assistant. Solve math problems step by step. "
                       "Use Python code in a single ```python code block to do the calculations, "
                       "and print the results. After the code has run, give the final answer "
                       "in \\boxed{} and then reply with TERMINATE.",
    )

    code_executor = LocalCommandLineCodeExecutor(work_dir="coding")
    math_proxy_agent = CodeExecutorAgent("math_proxy_agent", code_executor=code_executor)

    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(12)
    team = RoundRobinGroupChat([assistant, math_proxy_agent], termination_condition=termination)

    # the math problem and initiate chat
    # math_problem = (
    #     """
    #     Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$.
    #     Express your answer in interval notation.
    #     """
    # )

    math_problem = "Problem: If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what is the value of $x - y$ ?"
    try:
        await Console(team.run_stream(task=math_problem))
    finally:
        await code_executor.stop()
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
