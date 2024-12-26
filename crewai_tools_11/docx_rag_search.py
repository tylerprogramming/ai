from crewai_tools import DOCXSearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# For fixed directory searches
tool = DOCXSearchTool(docx='./rag_dir/user.docx')

# Create an agent with the knowledge store
agent = Agent(
    role="DOCX Search Agent",
    goal="You will search the DOCX file for the answer to the question.  Use the tools to search the DOCX file.",
    backstory="""You are a master at searching DOCX files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False
)
task = Task(
    description="Answer the following questions about the DOCX file: {question}",
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
    question = input("Enter a question about the DOCX file: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)