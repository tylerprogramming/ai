from crewai_tools import ExaSearchTool, ScrapeWebsiteTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

tool = ExaSearchTool()
scrape_tool = ScrapeWebsiteTool()

llm = LLM(model="gpt-5.4-mini")

agent = Agent(
    role="EXA Search Agent",
    goal="You will search the website based on the input and then scrape those websites.",
    backstory="""You are a master at searching websites.""",
    tools=[tool, scrape_tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following questions about the website: {question}",
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
    question = input("Input: ")
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)