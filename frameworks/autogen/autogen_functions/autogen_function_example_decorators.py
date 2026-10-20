import asyncio
import os

import dotenv
from typing import Literal
from typing_extensions import Annotated
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

dotenv.load_dotenv()  # OPENAI_API_KEY (and optionally "model") from .env

CurrencySymbol = Literal["USD", "EUR"]


def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.09
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


# In v0.7 there are no decorators: the type hints, Annotated descriptions and docstring
# of a plain function are enough. Just pass it to the agent with tools=[...].
def currency_calculator(
        base_amount: Annotated[float, "Amount of currency in base_currency"],
        base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
        quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    """Currency exchange calculator."""
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    return f"{quote_amount} {quote_currency}"


async def main():
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("model", "gpt-5.4-mini"),
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )

    currency_bot = AssistantAgent(
        name="currency_bot",
        model_client=model_client,
        tools=[currency_calculator],
        reflect_on_tool_use=True,  # after calling the tool, the bot answers with the result
        system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE "
                       "when the task is done.",
    )

    # start the conversation
    await Console(currency_bot.run_stream(task="How much is 123.45 USD in EUR?"))
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
