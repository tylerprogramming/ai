from pydantic import  BaseModel
from typing import Literal
from helpers.run_llm import run_llm
from helpers.json_llm import JSON_llm

task = """
Implement a Stack with:
1. push(x)
2. pop()
3. getMin()
All operations should be O(1).
"""

GENERATOR_PROMPT = """
Your goal is to complete the task based on <user input>. If there are feedback 
from your previous generations, you should reflect on them to improve your solution

Output your answer concisely in the following format: 

Thoughts:
[Your understanding of the task and feedback and how you plan to improve]

Response:
[Your code implementation here]
"""

def generate(task: str, generator_prompt: str, context: str = "") -> tuple[str, str]:
    """Generate and improve a solution based on feedback."""
    full_prompt = f"{generator_prompt}\n{context}\nTask: {task}" if context else f"{generator_prompt}\nTask: {task}"

    response = run_llm(full_prompt, model="gpt-4o")
    
    print("\n## Generation start")
    print(f"Output:\n{response}\n")
    
    return response

EVALUATOR_PROMPT = """
Evaluate this following code implementation for:
1. code correctness
2. time complexity
3. style and best practices

You should be evaluating only and not attempting to solve the task.

Only output "PASS" if all criteria are met and you have no further suggestions for improvements.

Provide detailed feedback if there are areas that need improvement. You should specify what needs improvement and why.

Only output JSON.
"""

def evaluate(task : str, evaluator_prompt : str, generated_content: str) -> tuple[str, str]:
    """Evaluate if a solution meets requirements."""
    full_prompt = f"{evaluator_prompt}\nOriginal task: {task}\nContent to evaluate: {generated_content}"

    #Build a schema for the evaluation
    class Evaluation(BaseModel):
        evaluation: Literal["PASS", "NEEDS_IMPROVEMENT", "FAIL"]
        feedback: str

    response = JSON_llm(full_prompt, Evaluation)
    
    evaluation = response["evaluation"]
    feedback = response["feedback"]

    print("## Evaluation start")
    print(f"Status: {evaluation}")
    print(f"Feedback: {feedback}")

    return evaluation, feedback

def loop_workflow(task: str, evaluator_prompt: str, generator_prompt: str) -> tuple[str, list[dict]]:
    """Keep generating and evaluating until the evaluator passes the last generated response."""
    # Store previous responses from generator
    memory = []
    
    # Generate initial response
    response = generate(task, generator_prompt)
    memory.append(response)

   
    # While the generated response is not passing, keep generating and evaluating
    while True:
        evaluation, feedback = evaluate(task, evaluator_prompt, response)
        # Terminating condition
        if evaluation == "PASS":
            return response
        
        # Add current response and feedback to context and generate a new response
        context = "\n".join([
            "Previous attempts:",
            *[f"- {m}" for m in memory],
            f"\nFeedback: {feedback}"
        ])
        
        response = generate(task, generator_prompt, context)
        memory.append(response)

loop_workflow(task, EVALUATOR_PROMPT, GENERATOR_PROMPT)