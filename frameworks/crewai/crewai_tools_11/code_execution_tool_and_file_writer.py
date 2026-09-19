from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import CodeInterpreterTool, FileWriterTool
from dotenv import load_dotenv

load_dotenv()

tool = CodeInterpreterTool()
file_writer = FileWriterTool()

agent = Agent(
    role="Code Execution Agent",
    goal="You will execute the code and return the output AND save the code to the proper directory given by the tool.",
    backstory="""You are a master at executing code.""",
    tools=[tool, file_writer],
    verbose=True,
    allow_delegation=False,
)

task = Task(
    description="Answer the following question: {question}",
    expected_output="The actual code used to get the answer to the file.  Save the code to the proper directory.  ONLY save the code.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)


question = input("Enter your code question: ")
result = crew.kickoff(inputs={"question": question})
print(result)