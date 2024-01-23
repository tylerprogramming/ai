import os
from crewai import Agent, Task, Crew, Process
from langchain.llms import Ollama

# used for Ollama and a local model
ollama_openhermes = Ollama(model="openhermes")

# either use api key for gpt, or just some string for local
os.environ["OPENAI_API_KEY"] = "sk-1111"


# Create a researcher agent
researcher = Agent(
    role='Senior Researcher',
    goal='Discover groundbreaking technologies',
    backstory='A curious mind fascinated by cutting-edge innovation and the potential to change the world, '
              'you know everything about tech.',
    verbose=True,
    llm=ollama_openhermes
)

# Create a writer agent
writer = Agent(
    role='Writer',
    goal='Craft compelling stories about tech discoveries',
    verbose=True,
    backstory='A creative soul who translates complex tech jargon into engaging narratives for the masses, you write '
              'using simple words in a friendly and inviting tone that does not sounds like AI.',
    llm=ollama_openhermes
)

# Task for the researcher
research_task = Task(
    description='Identify the next big trend in AI',
    agent=researcher  # Assigning the task to the researcher
)

# Task for the writer
write_task = Task(
    description='Write an article on AI advancements leveraging the research made.',
    agent=writer  # Assigning the task to the writer
)

# Instantiate your crew with a sequential process
tech_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Tasks will be executed one after the other
    llm=ollama_openhermes
)

# Get your crew to work!
result = tech_crew.kickoff()

print("######################")
print(result)
