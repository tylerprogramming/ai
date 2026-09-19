from crewai_tools import FileReadTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# For fixed directory searches
tool = FileReadTool()

# Create an agent with the knowledge store
agent = Agent(
    role="File Read Agent",
    goal="You will read the file for the answer to the question.  Use the tools to read the file.",
    backstory="""You are a master at reading files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False
)
task = Task(
    description="What's in this file: {question}",
    expected_output="An answer to the question.",
    tools=[tool],
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

while True:
    question = input("The file is: ")
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)