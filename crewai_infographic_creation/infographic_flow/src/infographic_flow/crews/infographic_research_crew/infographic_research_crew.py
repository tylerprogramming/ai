from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class InfographicKeypoint(BaseModel):
    keypoint: str
    image_name: str

class InfographicKeypointList(BaseModel):
    infographic_keypoints: list[InfographicKeypoint]

@CrewBase
class InfographicResearchCrew:
    """Infographic Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def infographic_researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["infographic_researcher_agent"],
        )

    @agent
    def infographic_keypoints_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["infographic_keypoints_agent"],
        )

    @task
    def infographic_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["infographic_research_task"],
        )

    @task
    def infographic_keypoints_task(self) -> Task:
        return Task(
            config=self.tasks_config["infographic_keypoints_task"],
            output_pydantic=InfographicKeypointList
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Infographic Research Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
