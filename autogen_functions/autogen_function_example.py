from typing import Literal

import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"]
    },
)

llm_config = {
    "functions": [
        {
            "name": "currency_calculator",
            "description": "Currency exchange calculator.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_amount": {
                        "type": "string",
                        "description": "the base amount",
                    },
                    "base_currency": {
                        "type": "string",
                        "description": "the base currency",
                    },
                    "quote_currency": {
                        "type": "string",
                        "description": "the quote currency",
                    },
                },
                "required": ["base_amount", "base_currency", "quote_currency"],
            },
        },
    ],
    "config_list": config_list,
    "timeout": 120,
}


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
        base_amount=0.0,
        base_currency="USD",
        quote_currency="EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * float(base_amount)
    return f"{quote_amount} {quote_currency}"


currency_bot = autogen.AssistantAgent(
    name="currency_bot",
    system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE "
                   "when the task is done.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)

CurrencySymbol = Literal["USD", "EUR"]

# register the functions
user_proxy.register_function(
    function_map={
        "currency_calculator": currency_calculator
    }
)

# start the conversation
user_proxy.initiate_chat(
    currency_bot,
    message="How much is 123.45 USD in EUR?",
)
