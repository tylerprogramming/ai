"""
PydanticAI Tools with Context Example

Tools with dependency injection and runtime context.
"""

from dataclasses import dataclass
from pydantic_ai import Agent, RunContext


@dataclass
class UserContext:
    """Runtime context with user-specific data."""
    user_id: str
    user_name: str
    preferences: dict


user_database = {
    "user_123": {"name": "Alice", "favorite_color": "blue", "location": "NYC"},
    "user_456": {"name": "Bob", "favorite_color": "green", "location": "LA"},
}


agent = Agent(
    "openai:gpt-5.4-mini",
    deps_type=UserContext,
    system_prompt="You are a personalized assistant. Use the user's preferences to tailor responses.",
)


@agent.tool
async def get_user_preference(
    ctx: RunContext[UserContext], preference_key: str
) -> str:
    """Get a specific user preference."""
    user_data = user_database.get(ctx.deps.user_id, {})
    return user_data.get(preference_key, "Not set")


@agent.tool
async def update_preference(
    ctx: RunContext[UserContext], key: str, value: str
) -> str:
    """Update a user preference."""
    if ctx.deps.user_id in user_database:
        user_database[ctx.deps.user_id][key] = value
        return f"Updated {key} to {value} for {ctx.deps.user_name}"
    return "User not found"


@agent.tool
async def list_all_preferences(ctx: RunContext[UserContext]) -> dict:
    """List all preferences for the current user."""
    return user_database.get(ctx.deps.user_id, {})


async def main():
    context = UserContext(
        user_id="user_123",
        user_name="Alice",
        preferences=user_database["user_123"],
    )

    result = await agent.run(
        "What's my favorite color? Also, update my location to San Francisco.",
        deps=context,
    )

    print(f"Response: {result.data}")
    print(f"\nUpdated database: {user_database['user_123']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
