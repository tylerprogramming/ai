#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from item_picker.crew import ItemPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
def evaluate(task : str, evaluator_prompt : str, response_to_evaluate: str) -> tuple[str, str]:
    """Evaluate if a solution meets requirements."""
    #Build a schema for the evaluation
    class Evaluation(BaseModel):
        evaluation: Literal["PASS", "NEEDS_IMPROVEMENT", "FAIL"]
        feedback: str
        
    agent = Agent(
        role="Evaluator",
        goal="Evaluate the given content against the provided criteria.",
        backstory="You are an expert evaluator who provides detailed feedback on the quality of the content.",
        output_pydantic=Evaluation,
    )
    task = Task(
        description=evaluator_prompt,
        expected_output="A JSON object with the evaluation and feedback.",
        agent=agent,
    )
    crew = Crew(
        tasks=[task],
        agents=[agent],
    )
    
    response = crew.kickoff(inputs=generated_content)
    
    full_prompt = f"{evaluator_prompt}\nOriginal task: {task}\nContent to evaluate: {generated_content}"

    

    response = JSON_llm(full_prompt, Evaluation)
    
    evaluation = response["evaluation"]
    feedback = response["feedback"]

    print("## Evaluation start")
    print(f"Status: {evaluation}")
    print(f"Feedback: {feedback}")

    return evaluation, feedback

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year),
        'context': ''
    }
    
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

    memory = []

    
    try:
        response = ItemPicker().crew().kickoff(inputs=inputs)
        memory.append(response)
        
        # While the generated response is not passing, keep generating and evaluating
        while True:
            evaluation, feedback = evaluate(response)
            # Terminating condition
            if evaluation == "PASS":
                return response
            
            # Add current response and feedback to context and generate a new response
            context = "\n".join([
                "Previous attempts:",
                *[f"- {m}" for m in memory],
                f"\nFeedback: {feedback}"
            ])
            inputs['context'] = context
            
            response = ItemPicker().crew().kickoff(inputs=inputs)
            memory.append(response)
            
        while True:
            pass
            # another crew to evaluate the next response
            
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
