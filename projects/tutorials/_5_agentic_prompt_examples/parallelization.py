import asyncio
from typing import List
from helpers.run_llm import run_llm
from helpers.async_run_llm import run_llm_parallel

async def parallel_workflow(prompt : str, proposer_models : List[str], aggregator_model : str, aggregator_prompt: str):
    """Run a parallel chain of LLM calls to address the `input_query` 
    using a list of models specified in `models`.

    Returns output from final aggregator model.
    """

    # Asynchronously call the function for each prompt
    tasks = [run_llm_parallel(prompt, model) for model in proposer_models]

    # Gather and run the tasks concurrently
    proposed_responses = await asyncio.gather(*tasks)
    
    # Aggregate responses using an aggregator model
    final_output = run_llm(
        user_prompt=prompt + "\n" + "\n".join(
            (f"{i+1}. {str(element)}" for i, element in enumerate(proposed_responses))
        ),
        model=aggregator_model
    )
    
    return final_output, proposed_responses


reference_models = [
    "o1-mini",
    "o1-preview"
]

user_prompt = """Jenna and her mother picked some apples from their apple farm. 
Jenna picked half as many apples as her mom. If her mom got 20 apples, how many apples did they both pick?"""

aggregator_model = "o1-mini"

aggregator_system_prompt = """You have been provided with a set of responses from various open-source models to the latest user query.
Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information
provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the
given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured,
coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""

async def main():
    answer, intermediate_reponses = await parallel_workflow(prompt = user_prompt, 
                                                            proposer_models = reference_models, 
                                                            aggregator_model = aggregator_model, 
                                                            aggregator_prompt = aggregator_system_prompt)

    for i, response in enumerate(intermediate_reponses):
        print(f"Intermetidate Response {i+1}:\n\n{response}\n")

    print(f"Final Answer: {answer}\n")


asyncio.run(main())