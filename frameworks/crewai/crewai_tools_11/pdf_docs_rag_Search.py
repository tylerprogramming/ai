from crewai_tools import PDFSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent

tool = PDFSearchTool(pdf=str(BASE_DIR / "pdf" / "AutoGen_Studio-12.pdf"))

# GPT-5 models only accept the default temperature (temperature=0 is rejected)
llm = LLM(model="gpt-5.4-mini")

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
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)

