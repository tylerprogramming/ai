import asyncio
from typing import Annotated

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

load_dotenv()  # OPENAI_API_KEY from .env


def exchange_rate(base_currency, quote_currency) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.09
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


def currency_calculator(
        base_amount: Annotated[str, "the base amount"] = "0.0",
        base_currency: Annotated[str, "the base currency"] = "USD",
        quote_currency: Annotated[str, "the quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * float(base_amount)
    return f"{quote_amount} {quote_currency}"


# In v0.7 the tool's JSON schema is built from the function signature, so there's no
# hand-written "functions" list in llm_config anymore. FunctionTool lets us give it the
# name and description explicitly (this replaces register_function(function_map=...)).
currency_tool = FunctionTool(
    currency_calculator,
    name="currency_calculator",
    description="Currency exchange calculator.",
)


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )

    currency_bot = AssistantAgent(
        name="currency_bot",
        model_client=model_client,
        tools=[currency_tool],
        reflect_on_tool_use=True,  # after calling the tool, the bot answers with the result
        system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE "
                       "when the task is done.",
    )

    # start the conversation (the agent calls the tool and runs it itself, no user_proxy needed)
    await Console(currency_bot.run_stream(task="How much is 123.45 USD in EUR?"))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
