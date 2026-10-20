import asyncio
import json
import logging

import pandas as pd
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core import EVENT_LOGGER_NAME
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()  # OPENAI_API_KEY from .env

LOG_FILE = "logs.jsonl"


def start_logging(log_file=LOG_FILE):
    """AutoGen v0.7 logs structured events (including every LLM call) to a standard Python logger.
    Each event is written as one JSON line in the log file."""
    handler = logging.FileHandler(log_file, mode="w")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger = logging.getLogger(EVENT_LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return handler


def stop_logging(handler):
    logging.getLogger(EVENT_LOGGER_NAME).removeHandler(handler)
    handler.close()


# create function to get log: read the JSON lines back and keep only the LLM calls
def get_log(log_file=LOG_FILE, event_type="LLMCall"):
    data = []
    with open(log_file) as f:
        for line in f:
            try:
                event = str_to_dict(line)
            except json.JSONDecodeError:
                continue  # skip anything that isn't a JSON event
            if event.get("type") == event_type:
                data.append(event)
    return data


def str_to_dict(s):
    return json.loads(s)


async def main():
    # setup the model client
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        temperature=0,
    )

    # Start logging
    handler = start_logging()
    print("Started logging to " + LOG_FILE)

    # Create an agent and run it
    assistant = AssistantAgent(name="assistant", model_client=model_client)
    result = await Console(
        assistant.run_stream(task="What is the height of the Sears Tower? Only respond with the answer and terminate")
    )

    # Stop logging
    stop_logging(handler)
    await model_client.close()

    # Token usage straight from the run result
    prompt_tokens = sum(m.models_usage.prompt_tokens for m in result.messages if m.models_usage)
    completion_tokens = sum(m.models_usage.completion_tokens for m in result.messages if m.models_usage)
    print(f"\nTokens used: {prompt_tokens} prompt + {completion_tokens} completion = {prompt_tokens + completion_tokens}")

    # use pandas to get extra information from the log and print out to terminal
    log_data = get_log()
    if log_data:
        df = pd.DataFrame(log_data)
        df["total_tokens"] = df["prompt_tokens"] + df["completion_tokens"]
        df["request"] = df["messages"].apply(lambda msgs: msgs[-1].get("content") if msgs else None)
        df["response"] = df["response"].apply(
            lambda r: r.get("choices", [{}])[0].get("message", {}).get("content") if isinstance(r, dict) else r
        )
        print(df[["agent_id", "request", "response", "prompt_tokens", "completion_tokens", "total_tokens"]].to_string())
    else:
        print("No LLM calls found in " + LOG_FILE)


if __name__ == "__main__":
    asyncio.run(main())
