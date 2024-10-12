from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Day02Crew:
	"""Day02 crew"""

	ollama_1b = LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434")
	phi3 = LLM(model="ollama/phi3", base_url="http://localhost:11434")

	@agent
	def chuck_norris_joke_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['chuck_norris_joke_generator'],
			verbose=True,
			llm=self.ollama_1b
		)

	@agent
	def chuck_norris_joke_picker(self) -> Agent:
		return Agent(
			config=self.agents_config['chuck_norris_joke_picker'],
			verbose=True,
			llm=self.phi3
		)

	@task
	def generate_joke_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_joke_task'],
		)

	@task
	def pick_joke_task(self) -> Task:
		return Task(
			config=self.tasks_config['pick_joke_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Day02 crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)