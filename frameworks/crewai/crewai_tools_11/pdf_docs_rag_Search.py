from crewai_tools import PDFSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

tool = PDFSearchTool(pdf='/Users/tylerreed/_ai-projects/ai/crewai_tools_11/pdf/AutoGen_Studio-12.pdf')

# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o", temperature=0)

# Create an agent with the knowledge store
agent = Agent(
    role="PDF Search Agent",
    goal="You will search the PDF for the answer to the question.  Use the tools to search the PDF.",
    backstory="""You are a master at searching PDF documents.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following questions about the PDF: {question}",
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
    question = input("Enter a question about the pdf documentation: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)

