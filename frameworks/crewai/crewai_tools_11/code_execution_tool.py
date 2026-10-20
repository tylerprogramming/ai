from crewai import Agent, Task, Crew, Process, LLM
# CodeInterpreterTool was removed in crewai-tools 1.x; E2BPythonTool runs the code
# in an E2B cloud sandbox instead (needs E2B_API_KEY, see README)
from crewai_tools import E2BPythonTool
from dotenv import load_dotenv

load_dotenv()

tool = E2BPythonTool()

llm = LLM(model="gpt-5.4-mini")

agent = Agent(
    role="Code Execution Agent",
    goal="You will execute the code and return the output",
    backstory="""You are a master at executing code.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following question: {question}",
    expected_output="The actual code used to get the answer to the file.",
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