from typing import List

import autogen
import dotenv
from autogen import ChatResult

import config

dotenv.load_dotenv()

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="As the assistant agent, the question, multiple choice answers, the answer to the "
                   "question, and the reason should be put into json format and returned in proper format.",
    llm_config=config.llm_config,
)

json_assistant = autogen.AssistantAgent(
    name="json_assistant",
    system_message="As the json assistant agent, my only purpose is to take the response from the assistant "
                   "agent,"
                   "and format the question, multiple choices answers, the answer to the question and the "
                   "reason"
                   "and save them to a file.",
    llm_config=config.llm_config
)

converter = autogen.AssistantAgent(
    name="converter",
    system_message="I only convert the response given to me to json format, and that is all and return it.",
    llm_config=config.llm_config
)

# create a UserProxyAgent instance "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False,
    llm_config=config.llm_config
)


def initiate_agent_chats() -> List[ChatResult]:
    chat_result = user_proxy.initiate_chats(
        [
            {
                "recipient": assistant,
                "message": """
                            Find the answers to the question below from the {uploaded_file} and do not write any code.

                            1. Can you give me a multiple choice question from the pdf with 4 choices and 1 of them being 
                            the answer?  Also give the reason for the answer and the page it was found on. 2. Make all 
                            the choices under the property choices, and the answer to be called correct_answer
                            """,
                "clear_history": True,
                "silent": False,
            },
            {
                "recipient": converter,
                "message": """
                            The only job here is to convert the json from previous agent into json format 
                            and also remove newline characters and return updated json format.
                        """,
                "summary_method": "last_msg"
            },
            {
                "recipient": json_assistant,
                "message": """
                            Take the context from the assistant and convert it to json and save it to disk to a 
                            json file in this directory.
                         """,
                "summary_method": "reflection_with_llm",
                "carryover": "I want to save this to disk with the name tester.json"
            }
        ]
    )

    return chat_result
