from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class DeepFriedResponseCrew():
	"""Deep Fried Response Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def response_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['response_generator'],
		)

	@agent
	def response_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['response_checker'],
		)

	@task
	def response_generator_task(self) -> Task:
		return Task(
			config=self.tasks_config['response_generator'],
		)

	@task
	def response_checker_task(self) -> Task:
		return Task(
			config=self.tasks_config['response_checker'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
