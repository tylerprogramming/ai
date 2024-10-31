from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.function_tool import tool

@CrewBase
class MathCrew():
	"""MathCrew crew"""

	@agent
	def math_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['math_agent'],
			tools=[tool],
			verbose=True
		)
	
	@task
	def math_task(self) -> Task:
		return Task(
			config=self.tasks_config['math_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MathCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)