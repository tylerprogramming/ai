from crewai import Crew, Task, Process, Agent
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class MyCrew:
    """My First Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def my_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['my_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def emoji_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['emoji_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False,
        )
    
    @task
    def my_task(self) -> Task:
        return Task(
            config=self.tasks_config['my_task'],
            agent=self.my_agent(),
        )
    
    @task
    def emoji_task(self) -> Task:
        return Task(
            config=self.tasks_config['emoji_task'],
            agent=self.emoji_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential,
        )
    
    
    