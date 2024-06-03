import json
import os

import autogen
from dotenv import load_dotenv
from typing_extensions import Annotated

from _integrations.reddit.reddit_classes import RedditPostsLoader

load_dotenv()

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path="../.env",
    model_api_key_map={"gpt-3.5-turbo": os.getenv("OPENAI_API_KEY")}
)

llm_config = {
    "temperature": 0,
    "config_list": config_list,
    "cache_seed": 45
}

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
)

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Get a random subreddit")
def get_random_subreddit(
        mode: Annotated[str, "The mode to retrieve reddit posts from"],
        number_of_posts: Annotated[int, "The number of posts to retrieve, default should be 1"]
):
    loader = RedditPostsLoader(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="extractor by u/tyler_programming",
        categories=["new", "hot"],
        mode=mode,
        number_posts=number_of_posts,
    )

    reddit_readers = loader.load()

    serialized_data = json.dumps([reddit.serialize() for reddit in reddit_readers])

    return serialized_data


@user_proxy.register_for_execution()
@engineer.register_for_llm(description="Get a random subreddit")
def get_specified_subreddit(
        search_queries: Annotated[str, "The search queries comma separated"],
        number_of_posts: Annotated[int, "The number of posts to retrieve, default should be 1"]
):
    loader = RedditPostsLoader(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="extractor by u/tyler_programming",
        categories=["new"],
        mode="subreddit",
        search_queries=[
            search_queries
        ],
        number_posts=number_of_posts,
    )

    reddit_readers = loader.load()

    serialized_data = json.dumps([reddit.serialize() for reddit in reddit_readers])

    return serialized_data


chat_result = user_proxy.initiate_chat(
    engineer,
    message="""
        I need you to integrate with Reddit.  Whenever you retrieve a post, you will get a RedditReader Object list and
        I would like you to format the content and meta_data contained within.
        
        Metadata is in this format for each item in the list:
        
        reddit_list.post_subreddit,
        reddit_list.post_category,
        reddit_list.post_title,
        reddit_list.post_score,
        reddit_list.post_id,
        reddit_list.post_url,
        reddit_list.post_author
        
        Then also add the content from the item.
        
        Do not start until I give a command.
""",
)
