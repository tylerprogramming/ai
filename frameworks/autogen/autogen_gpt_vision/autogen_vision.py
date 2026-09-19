import autogen
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

image_goldendoodle = "https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0"
image_corgi = "https://cdn.pixabay.com/photo/2019/08/19/07/45/corgi-4415649_1280.jpg"
image_luigi_yoshi_mario = "https://cdn.pixabay.com/photo/2016/07/30/14/25/mario-1557240_1280.jpg"
image_super_nintendo = "https://cdn.pixabay.com/photo/2018/04/26/06/59/technology-3351286_1280.jpg"
image_mitochondria = "https://cdn.pixabay.com/photo/2021/07/18/05/36/cell-6474673_1280.jpg"
image_waldo = "https://i.stack.imgur.com/reNlF.jpg"

config_list_4v = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)

image_agent = MultimodalConversableAgent(
    name="image-explainer",
    llm_config={"config_list": config_list_4v, "temperature": 0.5, "max_tokens": 500}
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

# Example 1
user_proxy.initiate_chat(
    image_agent,
    message=f"""
        Can you please find waldo in this image? <img {image_waldo}>
    """
)

# Example 2
# user_proxy.initiate_chat(image_agent,
#                          message="""What is this picture of and describe everything in it?
# <img {image_goldendoodle}>""")
#
# user_proxy.send(
#     message=f"""
#         What dog is this a picture of? <img {image_corgi}>
#
#         Which of these dogs tends to bark more, this one or the previous dog image?
#     """,
#     recipient=image_agent
# )

# Example 3
# user_proxy.initiate_chat(image_agent,
#     message=f"""
#         What is this picture of and describe everything in it? <img {image_luigi_yoshi_mario}>
#     """)
#
# user_proxy.send(
#     message=f"""
#         What game is displayed here? <img {image_super_nintendo}>
#
#         Among all of these characters, which one has sold the most amount of games?  Can you also give some figures for all
#         characters shown?
#     """,
#     recipient=image_agent
# )
