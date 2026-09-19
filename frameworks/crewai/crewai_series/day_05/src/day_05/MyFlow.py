import asyncio

from crewai.flow.flow import Flow, listen, start, or_, and_
from litellm import completion
from dotenv import load_dotenv
import os
from crew import Day05Crew
from pydantic import BaseModel

load_dotenv()

class News(BaseModel):
    news: str = ""

class NewsFlow(Flow[News]):
    model = "gpt-4o-mini"
    model_4o = "gpt-4o"

    @start()
    def generate_news_topic(self):
        print("Starting flow")

        response = completion(
            model=self.model_4o,
            messages=[
                {
                    "role": "user",
                    "content": """Return a topic within the ai world that is trending.  
                    This should be 1 - 4 words.""",
                },
            ],
        )

        news_topic = response["choices"][0]["message"]["content"]

        print(f"News Topic: {news_topic}")

        return news_topic

    @listen(generate_news_topic)
    def generate_news(self, news_topic):
        print("Generating news with Crew")

        inputs = {
            'topic': news_topic
        }

        result = Day05Crew().crew().kickoff(inputs=inputs)

        # get raw output then save to state
        output = result.raw
        self.state.news = output

        return output

    @listen(generate_news)
    def save_news(self, news):
        print("Saving news")
        
        # Create the news directory if it doesn't exist
        news_dir = os.path.join(os.path.dirname(__file__), "..", "..", "news")
        os.makedirs(news_dir, exist_ok=True)
        
        # Save the news in the news directory
        news_file_path = os.path.join(news_dir, "news.md")
        with open(news_file_path, "w") as f:
            f.write(news)
        
        print(f"News saved to: {news_file_path}")

    @listen(generate_news)
    def generate_best_news(self, input):
        print("Generating best news")
        
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Choose the most important news from the following and return it: {input}",
                },
            ],
        )

        important_news = response["choices"][0]["message"]["content"]
        return important_news
    
    @listen(and_(generate_news_topic, generate_news, save_news, generate_best_news))
    def logger(self, result):
        print(f"Logger: {result}")
        print("*" * 100)
        print("News Complete!")


async def main():
    flow = NewsFlow()
    flow.plot("my_flow_plot")

    await flow.kickoff()

asyncio.run(main())
