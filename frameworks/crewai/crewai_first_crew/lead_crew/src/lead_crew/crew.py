from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.score_tool import calculate_lead_score   

from dotenv import load_dotenv

load_dotenv()

@CrewBase
class LeadCrew():
    """Lead Scoring Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agents ---------------------------------------------------------
    @agent
    def transcript_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['transcript_curator'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def lead_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_extractor'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def insight_prioritizer(self) -> Agent:
        return Agent(
            config=self.agents_config['insight_prioritizer'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def lead_scorer(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_scorer'],  # type: ignore[index]
            tools=[calculate_lead_score],
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],  # type: ignore[index]
            verbose=True,
        )

    # Tasks ----------------------------------------------------------
    @task
    def curate_transcript_task(self) -> Task:
        return Task(
            config=self.tasks_config['curate_transcript_task'],  # type: ignore[index]
        )

    @task
    def extract_structured_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_structured_data_task'],  # type: ignore[index]
        )

    @task
    def prioritize_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config['prioritize_insights_task'],  # type: ignore[index]
        )

    @task
    def score_lead_task(self) -> Task:
        return Task(
            config=self.tasks_config['score_lead_task'],  # type: ignore[index]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'],  # type: ignore[index]
            output_file='lead_report.md',
        )

    # Crew -----------------------------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )