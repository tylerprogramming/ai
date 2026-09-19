from typing import List
from helpers.run_llm import run_llm 

def prompt_chain_workflow(input_query: str, prompt_chain : List[str]) -> List[str]:
    """Run a prompt chain of LLM calls to address the `input_query` 
    using a list of prompts specified in `prompt_chain`.
    """
    response_chain = []
    response = input_query
    for i, prompt in enumerate(prompt_chain):
        print(f"Step {i+1}")
        response = run_llm(f"{prompt}\nInput:\n{response}", model='gpt-4o')
        response_chain.append(response)
        print(f"{response}\n")
    return response_chain

question = "AI Agentic frameworks are the future, or is it?"

prompt_chain = ["""Generate a sample speech, create a TED talk on the topic of 'The Future of AI Agents'.""",
                """Given the speech, ONLY talk about the action items for the audience to take away.""",
                """Given the speech, translate it into Dutch."""]

responses = prompt_chain_workflow(question, prompt_chain)

final_answer = responses[-1]