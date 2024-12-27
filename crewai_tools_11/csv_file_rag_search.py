from crewai_tools import CSVSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

tool = CSVSearchTool(csv='/Users/tylerreed/_ai-projects/ai/crewai_tools_11/Financial Sample Data.csv')

agent = Agent(
    role="CSV Search Agent",
    goal="You will search the CSV file for the answer to the question.  Use the tools to search the CSV file.",
    backstory="""You are a master at searching CSV files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
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


