from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from crewai_tools import LlamaIndexTool
from pydantic import ConfigDict

model_config = ConfigDict(arbitrary_types_allowed=True)

yahoo_spec = YahooFinanceToolSpec()
yahoo_tools = yahoo_spec.to_tool_list()
crewai_yahoo_tools = [LlamaIndexTool.from_tool(t) for t in yahoo_tools]

@CrewBase
class YahooCrew():
	"""Yahoo Finance Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def yahoo_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['yahoo_agent'],
			tools=crewai_yahoo_tools
		)

	@task
	def yahoo_result(self) -> Task:
		return Task(
			config=self.tasks_config['yahoo_result'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Yahoo Finance Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
