from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_llamaindex_tools.llamaindex_tools.src.llamaindex_tools.tools.math_function_tool import my_tools

@CrewBase
class MathCrew():
	"""MathCrew crew"""

	@agent
	def math_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['math_agent'],
			tools=my_tools,
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
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
	
if __name__ == "__main__":
	math_crew = MathCrew()
	math_crew.crew.kickoff()