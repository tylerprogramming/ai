"""
CrewAI v1.15+ Streaming Output Example

Real-time streaming responses from crew execution.
"""

from crewai import Agent, Task, Crew, Process, LLM


def main():
    llm = LLM(model="gpt-5.4-mini", temperature=0.7)

    analyst = Agent(
        role="Data Analyst",
        goal="Analyze trends and provide insights",
        backstory="Expert data analyst with strong analytical skills",
        llm=llm,
        verbose=True,
    )

    analysis_task = Task(
        description="""Analyze the current trends in AI development for 2026.
        Focus on:
        1. Major breakthroughs
        2. Industry adoption
        3. Emerging challenges
        4. Future predictions""",
        expected_output="Comprehensive analysis report with clear sections",
        agent=analyst,
    )

    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True,
    )

    print("Starting analysis with streaming output...\n")

    for chunk in crew.kickoff_for_each(inputs=[{"focus": "AI Agents"}, {"focus": "LLMs"}]):
        print(f"Completed analysis: {chunk}")


if __name__ == "__main__":
    main()
