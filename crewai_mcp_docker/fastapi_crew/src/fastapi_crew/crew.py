from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from mcp import StdioServerParameters
from typing import List

@CrewBase
class FastapiCrew():
    """FastapiCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    mcp_server_params = [
        StdioServerParameters(
            command="docker", 
            args=["run", "-i", "--rm", "context7-mcp"]
        ),
        StdioServerParameters(
            command="docker", 
            args=["run", "--rm", "-i", "-v", "mcp-test:/mcp", "mcp/sqlite", "--db-path", "/mcp/test.db"]
        ),
        StdioServerParameters(
            command="docker", 
            args=[
                "run",
                "-i",
                "--rm",
                "--mount", "type=bind,src=/path/to/crewai_mcp_docker,dst=/path/to/crewai_mcp_docker",
                "mcp/filesystem",
                "/path/to/crewai_mcp_docker"
            ]
        ),
    ]

    @agent
    def fastapi_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['fastapi_agent'], # type: ignore[index]
            tools=self.get_mcp_tools(),
            verbose=True
        )

    @agent
    def code_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_writer'], # type: ignore[index]
            tools=self.get_mcp_tools(),
            verbose=True
        )
        
    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'], # type: ignore[index]
            tools=self.get_mcp_tools(),
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def fastapi_task(self) -> Task:
        return Task(
            config=self.tasks_config['fastapi_task'], # type: ignore[index]
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'], # type: ignore[index]
            context=[self.fastapi_task()]
        )
        
    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task'], # type: ignore[index]
            context=[self.fastapi_task(),self.code_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FastapiCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
