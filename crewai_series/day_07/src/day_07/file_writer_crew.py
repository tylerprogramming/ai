from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.custom_file_writer_tool import CustomFileWriterTool

@CrewBase
class FileWriterCrew:
	"""File Writer crew"""
	
	agents_config = "config/filewriter/agents.yaml"
	tasks_config = "config/filewriter/tasks.yaml"

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			tools=[CustomFileWriterTool()],
			verbose=True
		)

	@task
	def write_task(self) -> Task:
		return Task(
			config=self.tasks_config['write_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the File Writer crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)