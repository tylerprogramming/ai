import os
import autogen
import dotenv
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config
from memgpt.presets.presets import DEFAULT_PRESET
from memgpt.constants import LLM_MAX_TOKENS

dotenv.load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND")

if LLM_BACKEND == "openai":
    model = os.getenv("model")

    # assertion check to make sure you exported or set the key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key, "You must set OPENAI_API_KEY to run this example"

    # This config is for AutoGen agents that are not powered by MemGPT
    config_list = [
        {
            "model": model,
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]

    # This config is for AutoGen agents that powered by MemGPT
    config_list_memgpt = [
        {
            "model": model,
            "context_window": LLM_MAX_TOKENS[model],
            "preset": DEFAULT_PRESET,
            "model_wrapper": None,
            # new to 0.2.6 - open specific
            "model_endpoint_type": "openai",
            "model_endpoint": "https://api.openai.com/v1",
            "openai_key": openai_api_key,
        },
    ]

elif LLM_BACKEND == "local":
    # Example using LM Studio on a local machine
    # You will have to change the parameters based on your setup

    # Non-MemGPT agents will still use local LLMs, but they will use the ChatCompletions endpoint
    config_list = [
        {
            "model": "NULL",  # not needed
            # NOTE: on versions of pyautogen < 0.2.0 use "api_base", and also uncomment "api_type"
            # "api_base": "http://localhost:1234/v1",
            # "api_type": "open_ai",
            "base_url": "http://localhost:1234/v1",
            "api_key": "NULL",  # not needed
        },
    ]

    # MemGPT-powered agents will also use local LLMs, but they need additional setup (also they use the Completions
    # endpoint)
    config_list_memgpt = [
        {
            "preset": DEFAULT_PRESET,
            "model": None,  # only required for Ollama, see: https://memgpt.readthedocs.io/en/latest/ollama/
            "context_window": 8192,  # the context window of your model (for Mistral 7B-based models, it's likely 8192)
            "model_wrapper": "airoboros-l2-70b-2.1",  # airoboros is the default wrapper and should work for most models
            "model_endpoint_type": "lmstudio",  # can use webui, ollama, llamacpp, etc.
            "model_endpoint": "http://localhost:1234/v1",  # the IP address of your LLM backend
        },
    ]

else:
    raise ValueError(LLM_BACKEND)

# If USE_MEMGPT is False, then this example will be the same as the official AutoGen repo
# (https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb)
# If USE_MEMGPT is True, then we swap out the "coder" agent with a MemGPT agent
USE_MEMGPT = False

# Set to True if you want to print MemGPT's inner workings.
DEBUG = False

interface_kwargs = {
    "debug": DEBUG,
    "show_inner_thoughts": True,
    "show_function_outputs": DEBUG,
}

llm_config = {"config_list": config_list, "seed": 42}
llm_config_memgpt = {"config_list": config_list_memgpt, "seed": 42}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat", "use_docker": False},
    human_input_mode="TERMINATE",  # needed?
    default_auto_reply="...",  # Set a default auto-reply message here (non-empty auto-reply is required for LM Studio)
)

# The agent playing the role of the product manager (PM)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
    default_auto_reply="...",  # Set a default auto-reply message here (non-empty auto-reply is required for LM Studio)
)

if not USE_MEMGPT:
    # In the AutoGen example, we create an AssistantAgent to play the role of the coder
    print("AutoGen Coder")
    coder = autogen.AssistantAgent(
        name="Coder",
        llm_config=llm_config,
    )

else:
    # In our example, we swap this AutoGen agent with a MemGPT agent
    # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
    coder = create_memgpt_autogen_agent_from_config(
        "MemGPT_coder",
        llm_config=llm_config_memgpt,
        system_message=f"I am a 10x engineer, trained in Python. I was the first engineer at Uber "
                       f"(which I make sure to tell everyone I work with).\n"
                       f"You are participating in a group chat with a user ({user_proxy.name}) "
                       f"and a product manager ({pm.name}).",
        interface_kwargs=interface_kwargs,
        default_auto_reply="...",
        # Set a default auto-reply message here (non-empty auto-reply is required for LM Studio)
        # skip_verify=False,
        # NOTE: you should set this to True if you expect your MemGPT AutoGen agent to call a function other than
        # send_message on the first turn
    )

# Initialize the group chat between the user and two LLM agents (PM and coder)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager,
    message="Create a simple random number generator in python, that's it."
)
