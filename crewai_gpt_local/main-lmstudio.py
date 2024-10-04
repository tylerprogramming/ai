from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Optional

@CrewBase
class ChuckNorrisCrew():
    """Chuck Norris Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def chuck_norris_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chuck_norris_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def chuck_norris_jokes_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['chuck_norris_jokes_picker'],
            tools=[],
            verbose=True,
            allow_delegation=False,
        )
    
    
    @task
    def chuck_norris_jokes_task(self) -> Task:
        return Task(
            config=self.tasks_config['chuck_norris_jokes_task'],
            agent=self.chuck_norris_agent()
        )
    
    @task
    def chuck_norris_jokes_picker_task(self) -> Task:
        return Task(
            config=self.tasks_config['chuck_norris_jokes_picker_task'],
            agent=self.chuck_norris_jokes_picker(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates a Chuck Norris Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    chuck_norris_crew = ChuckNorrisCrew()
    result = chuck_norris_crew.crew.kickoff()
    print(result)