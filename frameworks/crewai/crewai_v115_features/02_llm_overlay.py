"""
CrewAI v1.15+ LLM Overlay Example

Route different agent roles to different models for cost optimization.
"""

from crewai import Agent, Task, Crew, Process, LLM


def main():
    powerful_llm = LLM(model="gpt-5.4-mini", temperature=0.7)
    fast_llm = LLM(model="gpt-5.4-mini", temperature=0.3)

    strategist = Agent(
        role="Content Strategist",
        goal="Develop high-level content strategy",
        backstory="Senior strategist with 10 years of experience in content marketing",
        llm=powerful_llm,
        verbose=True,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write engaging content following the strategy",
        backstory="Skilled writer who creates compelling content",
        llm=fast_llm,
        verbose=True,
    )

    editor = Agent(
        role="Editor",
        goal="Polish and refine the content",
        backstory="Detail-oriented editor ensuring quality and consistency",
        llm=fast_llm,
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

    crew = Crew(
        agents=[strategist, writer, editor],
        tasks=[strategy_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "The Future of AI Agents in 2026"})
    print(f"\nFinal Output:\n{result}")


if __name__ == "__main__":
    main()
