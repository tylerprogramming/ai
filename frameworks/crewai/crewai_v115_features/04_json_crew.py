"""
CrewAI v1.15+ JSON Crew Definition Example

Define crews using JSON/YAML configuration for easy deployment.
"""

import json
from crewai import Crew


crew_config = {
    "agents": [
        {
            "role": "Senior Researcher",
            "goal": "Research and synthesize information on given topics",
            "backstory": "Expert researcher with PhD in Information Science",
            "verbose": True,
            "allow_delegation": False,
        },
        {
            "role": "Technical Writer",
            "goal": "Transform research into clear, engaging content",
            "backstory": "Award-winning technical writer with 15 years experience",
            "verbose": True,
            "allow_delegation": False,
        },
    ],
    "tasks": [
        {
            "description": "Research the topic: {topic}. Find key facts, trends, and insights.",
            "expected_output": "Comprehensive research notes with citations",
            "agent": "Senior Researcher",
        },
        {
            "description": "Write an article based on the research",
            "expected_output": "Well-structured article ready for publication",
            "agent": "Technical Writer",
        },
    ],
    "process": "sequential",
    "verbose": True,
}


def main():
    print("Crew Configuration:")
    print(json.dumps(crew_config, indent=2))
    print("\nNote: In production, use crewai.Crew.from_yaml() or from_json()")
    print("This example shows the configuration structure.\n")

    from crewai import Agent, Task, Crew, Process, LLM

    llm = LLM(model="gpt-5.4-mini")

    agents = {}
    for agent_config in crew_config["agents"]:
        agents[agent_config["role"]] = Agent(
            role=agent_config["role"],
            goal=agent_config["goal"],
            backstory=agent_config["backstory"],
            verbose=agent_config.get("verbose", True),
            allow_delegation=agent_config.get("allow_delegation", True),
            llm=llm,
        )

    tasks = []
    for task_config in crew_config["tasks"]:
        tasks.append(
            Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=agents[task_config["agent"]],
            )
        )

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "AI Agent Frameworks in 2026"})
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
