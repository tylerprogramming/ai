"""
CrewAI v1.15+ Streaming Output Example

Real-time streaming responses from crew execution.

With Crew(stream=True), kickoff() returns a CrewStreamingOutput: iterate it to
get chunks as the LLM produces them, then read .result for the final CrewOutput.
"""

from crewai import Agent, Task, Crew, Process, LLM


def main():
    # GPT-5 models only accept the default temperature, so none is set here
    llm = LLM(model="gpt-5.4-mini")

    analyst = Agent(
        role="Data Analyst",
        goal="Analyze trends and provide insights",
        backstory="Expert data analyst with strong analytical skills",
        llm=llm,
        verbose=False,  # keep the console clean so the streamed text is readable
    )

    analysis_task = Task(
        description="""Analyze the current trends in {focus} for 2026.
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
        stream=True,  # kickoff() now returns a stream instead of the final output
    )

    print("Starting analysis with streaming output...\n")

    streaming = crew.kickoff(inputs={"focus": "AI Agents"})
    for chunk in streaming:
        print(chunk.content, end="", flush=True)

    print(f"\n\nCompleted analysis:\n{streaming.result.raw}")


if __name__ == "__main__":
    main()
