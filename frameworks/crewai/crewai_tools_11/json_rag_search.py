from crewai_tools import JSONSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

# For fixed directory searches
tool = JSONSearchTool()

# Create an agent with the knowledge store
agent = Agent(
    role="JSON Search Agent",
    goal="You will search the JSON for the answer to the question.  Use the tools to search the JSON.",
    backstory="""You are a master at searching JSON files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False
)
task = Task(
    description="Answer the following questions about the JSON: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

while True:
    question = input("Enter a question about the JSON: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)