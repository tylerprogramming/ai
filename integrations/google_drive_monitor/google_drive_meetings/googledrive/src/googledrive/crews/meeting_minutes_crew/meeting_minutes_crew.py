from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool

# FileWriterTool no longer takes a fixed file name: the agent passes filename + directory
# (summary.txt / action_items.txt / sentiment.txt in meeting_minutes/) as the task describes.
file_writer_tool = FileWriterTool()

@CrewBase
class MeetingMinutesCrew():
	"""Meeting Minutes Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def meeting_minutes_summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['meeting_minutes_summarizer'],
			tools=[file_writer_tool],
		)
	
	@agent
	def meeting_minutes_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['meeting_minutes_writer'],
		)

	@task
	def meeting_minutes_summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['meeting_minutes_summary_task'],
		)

	@task
	def meeting_minutes_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['meeting_minutes_writing_task'],
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
