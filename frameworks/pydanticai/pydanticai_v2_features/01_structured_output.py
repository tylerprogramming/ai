"""
PydanticAI Structured Output Example

Type-safe agent responses using Pydantic models.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class MovieRecommendation(BaseModel):
    """A movie recommendation with details."""
    title: str = Field(description="The movie title")
    year: int = Field(description="Release year")
    genre: str = Field(description="Primary genre")
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    reason: str = Field(description="Why this movie is recommended")


class MovieList(BaseModel):
    """A list of movie recommendations."""
    recommendations: list[MovieRecommendation]
    theme: str = Field(description="Common theme among recommendations")


agent = Agent(
    "openai:gpt-5.4-mini",
    result_type=MovieList,
    system_prompt="You are a movie expert. Recommend movies based on user preferences.",
)


async def main():
    result = await agent.run(
        "Recommend 3 sci-fi movies from the 2020s that explore AI themes"
    )
    
    print(f"Theme: {result.data.theme}\n")
    for i, movie in enumerate(result.data.recommendations, 1):
        print(f"{i}. {movie.title} ({movie.year})")
        print(f"   Genre: {movie.genre}")
        print(f"   Rating: {movie.rating}/10")
        print(f"   Why: {movie.reason}\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
