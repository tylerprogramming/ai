from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_llamaindex_tools.llamaindex_tools.src.llamaindex_tools.tools.wiki_tool import WikipediaTool as wikipedia_tool

@CrewBase
class WikipediaCrew():
	"""Wikipedia Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def wikipedia_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['wikipedia_agent'],
			tools=[wikipedia_tool()]
		)

	@task
	def wikipedia_result(self) -> Task:
		return Task(
			config=self.tasks_config['wikipedia_result'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Wikipedia Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
