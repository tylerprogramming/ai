from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class QuoteCrew():
	"""Quote Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	@agent
	def quote_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['quote_writer'],
		)

	@task
	def write_quote(self) -> Task:
		return Task(
			config=self.tasks_config['write_quote'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Checklist Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
