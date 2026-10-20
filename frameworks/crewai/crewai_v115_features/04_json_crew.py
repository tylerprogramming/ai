"""
CrewAI v1.15+ JSON Crew Definition Example

Define crews using JSON configuration for easy deployment.

CrewAI builds the Agents, Tasks and Crew from the definition for you:
- load_crew_from_definition(dict)  -> an in-memory definition (this example)
- load_crew("crew.json")           -> a crew.json / crew.jsonc file, with one
                                       agents/<name>.json file per agent
Both return (crew, default_inputs).
"""

import json

from crewai.project.crew_loader import load_crew_from_definition


crew_config = {
    # Agents are keyed by name; tasks reference them by that name
    "agents": {
        "researcher": {
            "role": "Senior Researcher",
            "goal": "Research and synthesize information on given topics",
            "backstory": "Expert researcher with PhD in Information Science",
            "llm": "gpt-5.4-mini",
            "verbose": True,
            "allow_delegation": False,
        },
        "writer": {
            "role": "Technical Writer",
            "goal": "Transform research into clear, engaging content",
            "backstory": "Award-winning technical writer with 15 years experience",
            "llm": "gpt-5.4-mini",
            "verbose": True,
            "allow_delegation": False,
        },
    },
    "tasks": [
        {
            "name": "research_task",
            "description": "Research the topic: {topic}. Find key facts, trends, and insights.",
            "expected_output": "Comprehensive research notes with citations",
            "agent": "researcher",
        },
        {
            "name": "writing_task",
            "description": "Write an article based on the research",
            "expected_output": "Well-structured article ready for publication",
            "agent": "writer",
            "context": ["research_task"],
        },
    ],
    "process": "sequential",
    "verbose": True,
    # Default inputs; kickoff(inputs=...) values override them
    "inputs": {"topic": "AI Agent Frameworks in 2026"},
}


def main():
    print("Crew Configuration:")
    print(json.dumps(crew_config, indent=2))

    crew, default_inputs = load_crew_from_definition(crew_config)
    print(f"\nLoaded crew with agents: {[agent.role for agent in crew.agents]}\n")

    result = crew.kickoff(inputs=default_inputs)
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
