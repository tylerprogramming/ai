from crewai_tools import CSVSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent

tool = CSVSearchTool(csv=str(BASE_DIR / "Financial Sample Data.csv"))

llm = LLM(model="gpt-5.4-mini")

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
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)


