import autogen
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
import subprocess
import base64
import os

config_list_4v = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)

image_agent = MultimodalConversableAgent(
    name="image-explainer",
    llm_config={"config_list": config_list_4v, "temperature": 0.75, "max_tokens": 500}
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)


def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()


def create_screenshot(url, user_response_ss_name):
    print(f"Crawling {url}")

    if os.path.exists(user_response_ss_name):
        os.remove(user_response_ss_name)

    result = subprocess.run(
        ["node", "screenshot.js", url, user_response_ss_name],
        capture_output=True,
        text=True
    )

    exitcode = result.returncode

    if not exitcode == 0:
        print(f"Error with exitcode {exitcode} : {result.stderr}")
        return "ERROR"

    b64_image = image_b64(user_response_ss_name)
    return b64_image


def initiate_chat():
    user_response_url = input("What is the url you want to check?:")
    user_response_message = input("What do you want from this url?:")
    user_response_ss_name = input("What name do you want to give the screenshot?:")

    b64_image = create_screenshot(user_response_url, user_response_ss_name)

    if b64_image == "ERROR":
        return "I was unable to crawl that site, check error and try again."

    print("Image captured")

    # Example 1 - publix
    user_proxy.initiate_chat(
        image_agent,
        message=f"""
            What is this a picture of: <img {user_response_ss_name}>

            {user_response_message}
        """
    )

    # Example 2
    # user_proxy.initiate_chat(
    #     image_agent,
    #     message=f"""
    #             What is this a picture of: <img screenshot.jpg>
    #
    #             Can you give me a list of all the items and their prices from this image from amazon?.
    #         """
    # )


response = initiate_chat()

