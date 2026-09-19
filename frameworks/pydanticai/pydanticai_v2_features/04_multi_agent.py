"""
PydanticAI Multi-Agent Example

Coordinating multiple specialized agents.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class ResearchResult(BaseModel):
    """Research findings."""
    topic: str
    key_points: list[str]
    sources: list[str]


class ReviewResult(BaseModel):
    """Review of the research."""
    accuracy_score: float = Field(ge=0, le=10)
    completeness_score: float = Field(ge=0, le=10)
    suggestions: list[str]
    approved: bool


researcher = Agent(
    "openai:gpt-5.4-mini",
    result_type=ResearchResult,
    system_prompt="You are a thorough researcher. Gather key information on topics.",
)

reviewer = Agent(
    "openai:gpt-5.4-mini",
    result_type=ReviewResult,
    system_prompt="You are a critical reviewer. Evaluate research for accuracy and completeness.",
)


async def research_pipeline(topic: str) -> tuple[ResearchResult, ReviewResult]:
    """Run a research pipeline with researcher and reviewer agents."""
    research = await researcher.run(f"Research the topic: {topic}")
    
    review_prompt = f"""
    Review this research:
    Topic: {research.data.topic}
    Key Points: {research.data.key_points}
    Sources: {research.data.sources}
    """
    
    review = await reviewer.run(review_prompt)
    
    return research.data, review.data


async def main():
    topic = "The impact of AI agents on software development in 2026"
    
    print(f"Researching: {topic}\n")
    print("=" * 60)
    
    research, review = await research_pipeline(topic)
    
    print(f"\n📚 RESEARCH RESULTS")
    print(f"Topic: {research.topic}")
    print(f"\nKey Points:")
    for i, point in enumerate(research.key_points, 1):
        print(f"  {i}. {point}")
    print(f"\nSources: {', '.join(research.sources)}")
    
    print(f"\n\n📝 REVIEW")
    print(f"Accuracy: {review.accuracy_score}/10")
    print(f"Completeness: {review.completeness_score}/10")
    print(f"Approved: {'✅' if review.approved else '❌'}")
    print(f"\nSuggestions:")
    for suggestion in review.suggestions:
        print(f"  - {suggestion}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
