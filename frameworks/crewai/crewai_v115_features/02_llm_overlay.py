"""
CrewAI v1.15+ LLM Overlay Example

Route different agent roles to different models for cost optimization -
without editing the code that builds the agents.

Every agent below is declared on the cheap default model. At run time,
llm_overlay({role: model}) swaps the model for the roles you name; every
other agent keeps its declared llm. Use {"model:*": "<model>"} to put the
whole run on one model.
"""

from crewai import Agent, Task, Crew, Process, LLM
from crewai.llm_overlay import llm_overlay


def build_crew() -> Crew:
    # GPT-5 models only accept the default temperature, so none is set here
    llm = LLM(model="gpt-5.4-mini")

    strategist = Agent(
        role="Content Strategist",
        goal="Develop high-level content strategy",
        backstory="Senior strategist with 10 years of experience in content marketing",
        llm=llm,
        verbose=True,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write engaging content following the strategy",
        backstory="Skilled writer who creates compelling content",
        llm=llm,
        verbose=True,
    )

    editor = Agent(
        role="Editor",
        goal="Polish and refine the content",
        backstory="Detail-oriented editor ensuring quality and consistency",
        llm=llm,
        verbose=True,
    )

    strategy_task = Task(
        description="Create a content strategy for a blog post about {topic}",
        expected_output="Content strategy with key points, tone, and structure",
        agent=strategist,
    )

    writing_task = Task(
        description="Write the blog post following the strategy",
        expected_output="Complete blog post draft",
        agent=writer,
        context=[strategy_task],
    )

    editing_task = Task(
        description="Edit and polish the blog post",
        expected_output="Final polished blog post",
        agent=editor,
        context=[writing_task],
    )

    return Crew(
        agents=[strategist, writer, editor],
        tasks=[strategy_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
    )


def main():
    # Strategy needs the most reasoning -> bigger model; editing is simple -> smallest model.
    # The Content Writer is not listed, so it stays on its declared gpt-5.4-mini.
    overlay = {
        "Content Strategist": "gpt-5.4",
        "Editor": "gpt-5.4-nano",
    }

    # Build AND kick off the crew inside the block
    with llm_overlay(overlay):
        crew = build_crew()
        for agent in crew.agents:
            print(f"{agent.role:<20} -> {agent.llm.model}")
        result = crew.kickoff(inputs={"topic": "The Future of AI Agents in 2026"})

    print(f"\nFinal Output:\n{result}")


if __name__ == "__main__":
    main()
