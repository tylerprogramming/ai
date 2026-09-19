import autogen
import os
import http.client
import json

from pydantic import BaseModel, Field
from typing_extensions import Annotated
from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_API_KEY"))

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={"tags": ["4o-tool"]},
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}

newsapibot = autogen.AssistantAgent(
    name="newsapibot",
    system_message=f"For retrieving news articles, only use the functions you have been provided with.  Reply TERMINATE when the task is done.  The current time and date is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

serperbot = autogen.AssistantAgent(
    name="serperbot",
    system_message=f"For retrieving news articles, only use the functions you have been provided with.  Reply TERMINATE when the task is done.  The current time and date is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

news_aggregator = autogen.AssistantAgent(
    name="news_aggregator",
    system_message=f"You are an amazing news aggregator.  You create the best summaries with key points, sources, links, and descriptions. Make sure to get the news from every agent.  Reply TERMINATE when the task is done.",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

file_writer = autogen.AssistantAgent(
    name="file_writer",
    system_message=f"You are an amazing file writer.  You love writing to markdown files and creating them.  Make it look amazing!  Nice and clean, add emojis, make it pop!  Reply TERMINATE when the task is done.",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message=f"You are an amazing user.  You are done with the file_writer agent has finished writing the news articles to a markdown file.  You speak to all agents that can gather news.  You also must know the current date and time, which is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=15,
    code_execution_config=False,
)

class NewsAPIQuery(BaseModel):
    query: Annotated[str, Field(..., description="The query to search news articles for")]
    from_date: Annotated[str, Field(..., description="The from date to search news articles from", examples=["2024-09-21"])]
    to_date: Annotated[str, Field(..., description="The to date to search news articles from", examples=["2024-09-28"])]

@user_proxy.register_for_execution()
@newsapibot.register_for_llm(description="Retrieve news articles from newsapi.org.")
def retrieve_news_articles(news_api_query: Annotated[NewsAPIQuery, "The query to search for"]):
    """
    Retrieve news articles from newsapi.org.
    """
    
    all_articles = newsapi.get_everything(q=news_api_query.query,
                                      from_param=news_api_query.from_date,
                                      to=news_api_query.to_date,
                                      language='en',
                                      sort_by='relevancy',
                                      page_size=5)

    return all_articles


@user_proxy.register_for_execution()
@serperbot.register_for_llm(description="Retrieve news articles using serper.dev.")
def retrieve_news_serper(topic: Annotated[str, "The query to search for"]):
    """
    Retrieve news articles using serper.dev.
    """
    
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": topic,
        "num": 20,
        "tbs": "qdr:w"
    })
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

@user_proxy.register_for_execution()
@file_writer.register_for_llm(description="Write to a markdown file.")
def write_to_markdown_file(content: Annotated[str, "The content to write to the markdown file"]) -> str:
    """
    Write to a markdown file.
    """
    
    try:
        with open("news.md", "w") as f:
            f.write(content)
        return "success"
    except Exception as e:
        print(f"Failed to write to file: {str(e)}")
        return "failed"

    

chat_results = user_proxy.initiate_chats(
    [
        {
            "recipient": newsapibot,
            "message": "Can you get news articles on AI news from the last week?",
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        {
            "recipient": serperbot,
            "message": "Can you get news articles on AI Agents from the last week just using function retrieve_news_serper?",
            "summary_method": "last_msg",
        },
        {
            "recipient": news_aggregator,
            "message": "Can you summarize and make all the news articles from both agents?  also make a blogpost of the key points from the news articles!",
            "summary_method": "last_msg",
            "max_turns": 1
        },
        {
            "recipient": file_writer,
            "message": "Can you write the news articles to a markdown file?",
            "summary_method": "last_msg",
        },
    ]
)