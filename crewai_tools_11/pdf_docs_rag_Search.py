from crewai_tools import PDFSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"

# To specifically focus your search on a given documentation site 
# by providing its URL:
tool = PDFSearchTool(pdf='https://www.microsoft.com/en-us/research/uploads/prod/2024/08/AutoGen_Studio-12.pdf')

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
    question = input("Enter a question about the code documentation: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)

