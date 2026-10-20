import asyncio
import os
import http.client
import json

from pydantic import BaseModel, Field
from typing_extensions import Annotated
from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_API_KEY"))

class NewsAPIQuery(BaseModel):
    query: Annotated[str, Field(..., description="The query to search news articles for")]
    from_date: Annotated[str, Field(..., description="The from date to search news articles from", examples=["2024-09-21"])]
    to_date: Annotated[str, Field(..., description="The to date to search news articles from", examples=["2024-09-28"])]

# Tools are plain functions with type hints + a docstring; AutoGen v0.7 builds the schema from them
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


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        timeout=120,
    )

    # Each agent gets its tool directly (the old user_proxy only executed the function calls)
    newsapibot = AssistantAgent(
        name="newsapibot",
        system_message=f"For retrieving news articles, only use the functions you have been provided with.  Reply TERMINATE when the task is done.  The current time and date is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
        model_client=model_client,
        tools=[retrieve_news_articles],
        reflect_on_tool_use=True,
    )

    serperbot = AssistantAgent(
        name="serperbot",
        system_message=f"For retrieving news articles, only use the functions you have been provided with.  Reply TERMINATE when the task is done.  The current time and date is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
        model_client=model_client,
        tools=[retrieve_news_serper],
        reflect_on_tool_use=True,
    )

    news_aggregator = AssistantAgent(
        name="news_aggregator",
        system_message=f"You are an amazing news aggregator.  You create the best summaries with key points, sources, links, and descriptions. Make sure to get the news from every agent.  Reply TERMINATE when the task is done.",
        model_client=model_client,
    )

    file_writer = AssistantAgent(
        name="file_writer",
        system_message=f"You are an amazing file writer.  You love writing to markdown files and creating them.  Make it look amazing!  Nice and clean, add emojis, make it pop!  Reply TERMINATE when the task is done.",
        model_client=model_client,
        tools=[write_to_markdown_file],
        reflect_on_tool_use=True,
    )

    # The old initiate_chats ran these chats one after another, and each chat got the last
    # message of the earlier chats as carryover (summary_method="last_msg").
    chats = [
        (newsapibot, "Can you get news articles on AI news from the last week?"),
        (serperbot, "Can you get news articles on AI Agents from the last week just using function retrieve_news_serper?"),
        (news_aggregator, "Can you summarize and make all the news articles from both agents?  also make a blogpost of the key points from the news articles!"),
        (file_writer, "Can you write the news articles to a markdown file?"),
    ]

    carryover = []
    try:
        for agent, message in chats:
            task = message
            if carryover:
                task += "\nContext: \n" + "\n".join(carryover)
            result = await Console(agent.run_stream(task=task))
            carryover.append(result.messages[-1].to_text())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
