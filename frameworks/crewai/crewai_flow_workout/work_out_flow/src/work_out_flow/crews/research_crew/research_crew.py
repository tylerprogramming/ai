import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from composio_crewai import ComposioToolSet, Action, App
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
tools = composio_toolset.get_tools(actions=['FIRECRAWL_SEARCH', 'FIRECRAWL_CRAWL_URLS'])

class WorkOutResearch(BaseModel):
    research: str = ""
    links: list[str] = []   

@CrewBase
class ResearchCrew:
    """Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            output_pydantic=WorkOutResearch
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
