from crewai_tools import VisionTool
from crewai_tools import FileReadTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# For fixed directory searches
tool = VisionTool()

# Create an agent with the knowledge store
agent = Agent(
    role="Vision Agent",
    goal="You will read the image for the answer to the question.  Use the tools to read the image.",
    backstory="""You are a master at reading images.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False
)
task = Task(
    description="Answer the following questions about the image: {question}",
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
    user_input = input("Enter a question about the image: ")
    
    if user_input == "exit":
        break
    else:
        question = user_input
        
    result = crew.kickoff(inputs={"question": question})
    print(result)