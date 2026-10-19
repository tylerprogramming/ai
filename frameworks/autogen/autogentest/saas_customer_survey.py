import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini", temperature=0, timeout=300)

    engineer = AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the 
        code in a code block that specifies the script type. The user can't modify your code. So do not suggest 
        incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by 
        the executor. Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. 
        Check the execution result returned by the executor. If the result indicates there is an error, fix the error and 
        output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed 
        or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your 
        assumption, collect additional info you need, and think of a different approach to try.''',
    )

    planner = AssistantAgent(
        name="Planner",
        system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin 
        approval. The plan may involve an engineer who can write code and an executor and critic who doesn't write code. 
        Explain the plan first. Be clear which step is performed by an engineer, executor, and critic.''',
        model_client=model_client,
    )

    # Executes the Engineer's code blocks; generated files are saved in the "feedback" folder
    executor = CodeExecutorAgent(
        "Executor",
        code_executor=LocalCommandLineCodeExecutor(work_dir="feedback"),
        description="Executor. Execute the code written by the engineer and report the result.",
    )

    critic = AssistantAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback.",
        model_client=model_client,
    )

    # The model picks who speaks next (like the old GroupChatManager), up to 14 messages.
    # The old "Admin" user proxy only started the chat, so its message is now the task.
    team = SelectorGroupChat(
        participants=[engineer, planner, executor, critic],
        model_client=model_client,
        termination_condition=MaxMessageTermination(14),
    )

    await Console(team.run_stream(task="I would like to build a simple website that collects feedback from "
                                       "consumers via forms.  We can just use a flask application that creates an "
                                       "html website with forms and has a single question if they liked their "
                                       "customer experience and then keeps that answer.  I need a thank you html "
                                       "page once they completed the survey.  I then need a html page called "
                                       "admin that gives a nice table layout of all of the records from the "
                                       "database.  Just use sqlite3 as the database, keep it simple.  Also use "
                                       "Bootstrap for the CSS Styling."))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
