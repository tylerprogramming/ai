from crewai_tools import BaseTool
import json
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agentops.decorators import record_tool

load_dotenv()

class CustomSerperDevTool(BaseTool):
    name: str = "Serper Dev Tool"
    description: str = "A custom tool for searching on Serper Dev."

    @staticmethod
    @record_tool(tool_name="Serper Dev Tool")
    def extract_organic_results(json_data):
        # Parse the JSON data
        data = json.loads(json_data)
        
        # Extract the organic results
        news_results = data.get('news', [])
        
        # Create a list to store the extracted information
        extracted_info = []
    
        # Iterate through the news results
        for result in news_results:
            # Extract title, snippet, link, and imageUrl
            title = result['title']
            snippet = result['snippet']
            link = result['link']
            image_url = result['imageUrl']
            
            # Add the extracted information to the list
        extracted_info.append({
            'title': title,
            'snippet': snippet,
            'link': link,
            'image_url': image_url
        })
    
        return extracted_info

    def _run(self, search_query: str) -> str:
        url = "https://google.serper.dev/news"

        payload = json.dumps({
            "q": search_query,
            "num": 20,
            "tbs": "qdr:d",
            
        })
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        json_response = response.text

        # Extract the organic results from the JSON response
        organic_results = self.extract_organic_results(json_response)
        
        return json.dumps(organic_results, indent=2)

