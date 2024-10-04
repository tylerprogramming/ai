from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List, Optional
from crew_tool import CustomSerperDevTool\

class CustomSerperOutput(BaseModel):
    title: str
    snippet: str
    link: str
    image_url: str

class WebSearchOutput(BaseModel):
    title: str
    summary: str
    link: str
    image_url: str

class WebSearchOutputList(BaseModel):
    results: List[WebSearchOutput]

@CrewBase
class NewsAggregationCrew():
    """News Aggregation Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def ai_news_retriever(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_retriever'],
            tools=[CustomSerperDevTool()],
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def ai_news_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_summarizer'],
            tools=[ScrapeWebsiteTool()],
            verbose=True,
            allow_delegation=False,
        )
    
    
    @task
    def ai_news_retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_news_retrieval_task'],
            agent=self.ai_news_retriever(),
            output_json=CustomSerperOutput,
        )
    
    @task
    def ai_news_summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_news_summarization_task'],
            agent=self.ai_news_summarizer(),
            output_json=WebSearchOutputList,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates a News Aggregation Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_file='output.json',
        )