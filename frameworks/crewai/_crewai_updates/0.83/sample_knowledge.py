from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Create a knowledge source
content = "My name is Tyler. I am 36 years old and live in Florida.  Also, I rarely know what I'm doing and drink lots of coffee."
string_source = StringKnowledgeSource(
    content=content, metadata={"preference": "personal"}
)

# Create an agent with the knowledge store
agent = Agent(
    role="About User",
    goal="You know everything about the user.",
    backstory="""You are a master at understanding people and their preferences.""",
    verbose=True
)

task = Task(
    description="Answer the following questions about the user: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge={"sources": [string_source], "metadata": {"preference": "personal"}},
)

result = crew.kickoff(inputs={"question": "Where does Tyler live and what does he do?"})