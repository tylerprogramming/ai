from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, Action, App

load_dotenv()
import os

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
tools = composio_toolset.get_tools(
    actions=[
        'GOOGLECALENDAR_FIND_EVENT',
        'GOOGLECALENDAR_FIND_FREE_SLOTS',
        'GOOGLECALENDAR_CREATE_EVENT',
        'GOOGLECALENDAR_DELETE_EVENT',
        'GOOGLECALENDAR_UPDATE_EVENT'
    ]
)

gmail_tools = composio_toolset.get_tools(
    actions=[
        'GMAIL_SEND_EMAIL'
    ]
)
import os

load_dotenv()

@CrewBase
class GoogleCrew():
    """GoogleCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def google_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['google_agent'],
            tools=tools,
            verbose=True
        )
    
    @agent
    def gmail_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['gmail_agent'],
            tools=gmail_tools,
            verbose=True
        )

    @task
    def google_task(self) -> Task:
        return Task(
            config=self.tasks_config['google_task'],
        )

    @task
    def gmail_task(self) -> Task:
        return Task(
            config=self.tasks_config['gmail_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleCrew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
