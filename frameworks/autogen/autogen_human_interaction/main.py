import asyncio
import json

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

# if you ask it to save to disk first, it happens more often
message = """
Save the code to disk.

Can you write a total of 3 functions:

1. The first function takes in a string, and outputs the number of characters.
2. The second function checks a string to test if it is a palindrome.
3. The third function will take in a number, and return the square root of it.
"""


async def main():
    # the model client is the configuration for the LLM (openai, lm studio, ollama, etc.)
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        temperature=0.7,
    )

    # To use a local model in LM Studio instead (like the original 0.2 version did), swap in:
    # model_client = OpenAIChatCompletionClient(
    #     model="lmstudio",
    #     base_url="http://localhost:1234/v1",
    #     api_key="lm-studio",
    #     temperature=0.7,
    #     model_info={"vision": False, "function_calling": False, "json_output": False,
    #                 "family": "unknown", "structured_output": False},
    # )

    # the assistant agent takes in the name, and then the model client
    assistant = AssistantAgent(
        name="Assistant_Agent",
        model_client=model_client,
        system_message="You are a helpful AI assistant. Solve tasks using your coding and language skills. Write "
                       "python code in a code block, with '# filename: <filename>' as the first line when the code "
                       "should be saved to a file. Reply TERMINATE in the end when everything is done.",
    )

    # executes the code the assistant writes and saves it to the "tested_code" directory
    executor = CodeExecutorAgent(
        "executor",
        code_executor=LocalCommandLineCodeExecutor(work_dir="tested_code"),
    )

    # the user agent asks YOU for feedback every round (like human_input_mode="ALWAYS")
    # type feedback for the assistant, or "exit" to end the chat
    user = UserProxyAgent("User")

    # assistant writes code -> executor runs it -> you give feedback -> repeat
    termination = TextMentionTermination("TERMINATE", sources=["Assistant_Agent"]) | TextMentionTermination(
        "exit", sources=["User"])
    team = RoundRobinGroupChat([assistant, executor, user], termination_condition=termination)

    # this is how we execute our chat!
    result = await Console(team.run_stream(task=message))

    # like summary_method="reflection_with_llm": ask the LLM to summarize the conversation
    conversation = "\n".join(f"{m.source}: {m.to_text()}" for m in result.messages)
    summary = await model_client.create([
        UserMessage(
            content=conversation + "\n\nSummarize takeaway from the conversation. Do not add any introductory phrases. "
                                   "If the intended request is NOT properly addressed, please point it out.",
            source="user",
        )
    ])
    print("Summary:", summary.content)

    # this will dump the chat into a json file to look at
    json.dump([m.dump() for m in result.messages], open("conversations.json", "w"), indent=2)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
