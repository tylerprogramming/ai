from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

@CrewBase
class ChuckNorrisCrew():
    """Chuck Norris Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ollama_llama3_1b = LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434")
    ollama_phi3 = LLM(model="ollama/phi3", base_url="http://localhost:11434", temperature=0.1)
    lm_studio = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="sk-proj-1111")

    @agent
    def chuck_norris_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chuck_norris_agent'],
            tools=[SerperDevTool()],
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
            llm=self.lm_studio
        )
    
    @agent
    def chuck_norris_joke_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['chuck_norris_joke_creator'],
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self.lm_studio
        )
    
    @task
    def chuck_norris_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['chuck_norris_agent_task'],
            agent=self.chuck_norris_agent()
        )
    
    @task
    def chuck_norris_jokes_picker_task(self) -> Task:
        return Task(
            config=self.tasks_config['chuck_norris_jokes_picker_task'],
            agent=self.chuck_norris_jokes_picker(),
        )
    
    @task
    def chuck_norris_joke_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['chuck_norris_joke_creation_task'],
            agent=self.chuck_norris_joke_creator(),
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
    result = chuck_norris_crew.crew().kickoff()
    print(result)