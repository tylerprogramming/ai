from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

class Player(BaseModel):
    name: str
    age: int
    position: str
    team: str
    nationality: str
    summary: str

player_agent = Agent(
    role="Player Information Generator Agent About Futbol Players",
    goal="Generate information about the player: {name}",
    backstory="""You are an expert content creator, skilled in crafting engaging and informative blog posts.""",
    verbose=False,
    allow_delegation=False,
    llm="gpt-4o",
)

task1 = Task(
    description="""Find information on the given player and return a summary of the player's career.""",
    expected_output="Information about the player.",
    agent=player_agent,
    output_pydantic=Player,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[player_agent],
    tasks=[task1],
    verbose=True,
    process=Process.sequential,
)
inputs = {
    "name": "Lionel Messi",
}
result = crew.kickoff(inputs=inputs)
print(result)

# Accessing Properties Using Dictionary-Style Indexing
print("Futbol Player Information")
print("-------------------------\n")
name = result["name"]
age = result["age"]
position = result["position"]
team = result["team"]
nationality = result["nationality"]
summary = result["summary"]
print("Name:", name)
print("Age:", age)
print("Position:", position)
print("Team:", team)
print("Nationality:", nationality)
print("Summary:", summary)

# # Option 2: Accessing Properties Directly from the Pydantic Model
# print("Accessing Properties - Option 2")
# name = result.pydantic.name
# age = result.pydantic.age
# position = result.pydantic.position
# team = result.pydantic.team
# nationality = result.pydantic.nationality
# summary = result.pydantic.summary
# print("Name:", name)
# print("Age:", age)
# print("Position:", position)
# print("Team:", team)
# print("Nationality:", nationality)
# print("Summary:", summary)

# # Option 3: Accessing Properties Using the to_dict() Method
# print("Accessing Properties - Option 3")
# output_dict = result.to_dict()
# name = output_dict["name"]
# age = output_dict["age"]
# position = output_dict["position"]
# team = output_dict["team"]
# nationality = output_dict["nationality"]
# summary = output_dict["summary"]
# print("Name:", name)
# print("Age:", age)
# print("Position:", position)
# print("Team:", team)
# print("Nationality:", nationality)
# print("Summary:", summary)

# # Option 4: Printing the Entire Player Object
# print("Accessing Properties - Option 5")
# print("Player Information:", result)

