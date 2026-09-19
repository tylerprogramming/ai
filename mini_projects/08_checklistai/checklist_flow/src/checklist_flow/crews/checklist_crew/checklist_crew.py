from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ChecklistCrew():
	"""Checklist Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def checklist_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['checklist_writer'],
		)

	@task
	def write_checklist(self) -> Task:
		return Task(
			config=self.tasks_config['write_checklist'],
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
