from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import tools

@CrewBase
class AgenttestsCrew:
	"""agenttests crew"""

	# Agent definitions
	@agent
	def joke_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['joke_agent'],
			tools=[tools.write_to_memory, tools.read_from_memory, ],  # Pass in what tools this agent should have
			verbose=True
		)

	# Task definitions
	@task
	def create_a_joke(self) -> Task:
		return Task(
			config=self.tasks_config['create_a_joke'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Test crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)