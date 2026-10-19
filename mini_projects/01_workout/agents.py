from autogen_agentchat.agents import AssistantAgent

import config
import system_messages


async def create_workout_plan(days_option, selected_options, level_option):
    """Ask the fitness expert for a workout plan and return its reply."""
    model_client = config.create_model_client()

    # A new agent per request, so each workout plan starts with a fresh conversation
    fitness_expert = AssistantAgent(
        name=system_messages.fitness_expert_name,
        system_message=system_messages.fitness_expert_message,
        model_client=model_client,
    )

    try:
        result = await fitness_expert.run(
            task=system_messages.get_initiate_message(days_option, selected_options, level_option)
        )
    finally:
        await model_client.close()

    return result.messages[-1].content
