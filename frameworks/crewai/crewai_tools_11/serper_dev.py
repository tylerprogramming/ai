from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

# Create the tool with the token
tool = SerperDevTool()

llm = LLM(model="gpt-5.4-mini")

# Create an agent with the knowledge store
agent = Agent(
    role="Serper Search Agent",
    goal="You will search the internet for the answer to the question.  Use the tools to search the internet.",
    backstory="""You are a master at searching the internet.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following questions about the internet: {question}",
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
    question = input("Enter a question about the internet: ")
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)