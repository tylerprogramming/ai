import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import SourceMatchTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # GPT-5 models only accept the default temperature (and max_completion_tokens, not max_tokens), so the old GPT-4 sampling settings were dropped
        timeout=120,
    )

    coder = AssistantAgent(
        name="coder",
        model_client=model_client,
        system_message="""
    Make sure to save the code to disk.
    You are the Coder. Given a topic, write code to retrieve related papers from the arXiv API, 
    print their title, authors, abstract, and link. You write python/shell code to solve tasks. Wrap the code in a 
    code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code 
    which requires others to modify. Don't use a code block if it's not intended to be executed by the executor. 
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the 
    execution result returned by the executor. If the result indicates there is an error, fix the error and output 
    the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if 
    the task is not solved even after the code is executed successfully, analyze the problem, revisit your 
    assumption, collect additional info you need, and think of a different approach to try.
    """,
    )

    # Executor. Executes the code written by the Coder (saved in the "paper" folder) and reports the result.
    executor = CodeExecutorAgent(
        "executor",
        # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
        code_executor=LocalCommandLineCodeExecutor(work_dir="paper", cleanup_temp_files=False),
    )

    scientist = AssistantAgent(
        name="scientist",
        model_client=model_client,
        system_message="""You are the Scientist. Please categorize papers after seeing their abstracts printed and create 
    a markdown table with Domain, Title, Authors, Summary and Link""",
    )

    # Our own speaker selection: decides who talks next based on who spoke last.
    # The task message (source "user") plays the role of the old "Init" agent.
    def state_transition(messages):
        last_speaker = messages[-1].source

        if last_speaker == "user":
            return "coder"
        elif last_speaker == "coder":
            return "executor"
        elif last_speaker == "executor":
            # the code failed (or there was no code to run) -> back to the coder to fix it
            result = messages[-1].to_text()
            failed = (
                "exited with an error" in result
                or "No code blocks found" in result
                or ("produced no output" in result and "exit code was: 0" not in result)
            )
            if failed:
                return "coder"
            else:
                return "scientist"
        return None

    # The chat ends after the scientist has written the table (or after 20 messages)
    termination = SourceMatchTermination(["scientist"]) | MaxMessageTermination(20)

    groupchat = SelectorGroupChat(
        [coder, executor, scientist],
        model_client=model_client,
        selector_func=state_transition,
        termination_condition=termination,
    )

    await Console(groupchat.run_stream(
        task="Topic: LLM applications papers from last week. Requirement: 5 - 10 papers from different domains."
    ))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
