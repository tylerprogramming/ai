import os
from crewai import Crew, Process, Agent, Task   
from mem0 import MemoryClient
from search_mem0_tool import SearchMem0Tool

# Step 1: Record preferences based on past conversation or user input
client = MemoryClient(api_key="m0-sblhjtHFcj96vR7GAvPwQ5sVgY5J5pifrYrybXLA")

# Create an agent with the knowledge store
agent = Agent(
    role="About User",
    goal="You know everything about the user.",
    backstory="""You are a master at understanding people and their preferences.""",
    verbose=True
)

task = Task(
    description="Answer the following questions about the user: {question}.  Make sure to use the SearchMem0Tool to search the memory store for information to answer.",
    expected_output="An answer to the question.",
    agent=agent,
    tools=[SearchMem0Tool()]
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

while True:
    question = input("Enter a question: ")
    result = crew.kickoff(inputs={"question": question})
    print(f"Result: {result}")

    client.add(question, user_id="tyler", output_format="v1.1")
