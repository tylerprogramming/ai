import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

# configuration
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
)

llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
}

# create assistants
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=llm_config
)


math_proxy_agent = MathUserProxyAgent(
    name="math_proxy_agent",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

# the math problem and initiate chat
# math_problem = (
#     """
#     Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$.
#     Express your answer in interval notation.
#     """
# )

math_problem = "Problem: If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what is the value of $x - y$ ?"
math_proxy_agent.initiate_chat(assistant, problem=math_problem)
