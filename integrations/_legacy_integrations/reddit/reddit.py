import asyncio
import json
import os

from dotenv import load_dotenv
from typing_extensions import Annotated

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from reddit_classes import RedditPostsLoader

load_dotenv()  # OPENAI_API_KEY, CLIENT_ID, CLIENT_SECRET from .env (this folder or a parent folder)


# Tools: plain Python functions with type hints + docstrings. The docstring is the tool description.
def get_random_subreddit(
        mode: Annotated[str, "The mode to retrieve reddit posts from"],
        number_of_posts: Annotated[int, "The number of posts to retrieve, default should be 1"]
) -> str:
    """Get a random subreddit"""
    loader = RedditPostsLoader(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="extractor by u/tyler_programming",
        categories=["hot"],
        mode=mode,
        number_posts=number_of_posts,
    )

    reddit_readers = loader.load()

    serialized_data = json.dumps([reddit.serialize() for reddit in reddit_readers])

    return serialized_data


def get_specified_subreddit(
        search_queries: Annotated[str, "The search queries comma separated"],
        number_of_posts: Annotated[int, "The number of posts to retrieve, default should be 1"]
) -> str:
    """Get a specified subreddit"""
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


async def run_engineer(task: str) -> str:
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # temperature=0 removed: gpt-5 models only accept the default temperature
    )

    engineer = AssistantAgent(
        name="Engineer",
        model_client=model_client,
        tools=[get_random_subreddit, get_specified_subreddit],
        # after calling a tool, the agent formats the result (the JSON the Streamlit app reads)
        reflect_on_tool_use=True,
        system_message="""
        I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
        """,
    )

    result = await engineer.run(task=task)
    await model_client.close()

    # the last message is the agent's final answer (what chat_result.summary was in AutoGen 0.2)
    return result.messages[-1].content


def start_chat(input: str):
    # Streamlit calls this synchronously, so run the async agent with asyncio.run
    return asyncio.run(run_engineer(f"""
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
            
            Return this in proper json format, do not use triple tick marks to denote that it's json.  If there is more 
            than 1 object, make sure it's an array.
            
        [
            {{
        "meta_data": {{
            "subreddit": the subreddit,
            "category": the category,
            "title": the title,
            "score": the score,
            "post_id": the post id,
            "url": the url,
            "author": the author
            }},
            "content": the content
            }}
        ]
            
        {input}
    """))
