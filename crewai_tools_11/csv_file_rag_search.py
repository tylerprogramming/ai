from crewai_tools import CSVSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

# To specifically focus your search on a given documentation site 
# by providing its URL:
tool = CSVSearchTool(csv='/Users/tylerreed/_ai-projects/ai/crewai_tools_15/Financial Sample Data.csv')

# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o", temperature=0)

# Create an agent with the knowledge store
agent = Agent(
    role="CSV Search Agent",
    goal="You will search the CSV file for the answer to the question.  Use the tools to search the CSV file.",
    backstory="""You are a master at searching CSV files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following questions about the CSV file: {question}",
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
    question = input("Enter a question about the CSV file: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)


