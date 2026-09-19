from crewai_tools import BaseTool
import requests
import json
import os
from dotenv import load_dotenv
from agentops import record_tool

load_dotenv()

class CustomSerperDevTool(BaseTool):
    name: str = "Custom Serper Dev Tool"
    description: str = "Search the internet for news."

    @record_tool(tool_name="My own google search tool")
    def _run(self, query: str) -> str:
        """
        Search the internet for news.
        """

        url = "https://google.serper.dev/news"

        payload = json.dumps({
            "q": query,
            "num": 20,
            "autocorrect": False,
            "tbs": "qdr:d"
        })

        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Parse the JSON response
        response_data = response.json()

        # Extract only the 'news' property
        news_data = response_data.get('news', [])

        # Convert the news data back to a JSON string
        return json.dumps(news_data, indent=2)

