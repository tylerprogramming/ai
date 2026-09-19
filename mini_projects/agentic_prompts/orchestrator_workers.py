import asyncio
import json
from pydantic import BaseModel, Field
from typing import Literal, List
from helpers.async_run_llm import run_llm_parallel
from helpers.json_llm import JSON_llm

ORCHESTRATOR_PROMPT = """
Analyze this task and break it down into 2-3 distinct approaches:

Task: {task}

Provide an Analysis:

Explain your understanding of the task and which variations would be valuable.
Focus on how each approach serves different aspects of the task.

Along with the analysis, provide 2-3 approaches to tackle the task, each with a brief description:

Formal style: Write technically and precisely, focusing on detailed specifications
Conversational style: Write in a friendly and engaging way that connects with the reader
Hybrid style: Tell a story that includes technical details, combining emotional elements with specifications

Return only JSON output.
"""

WORKER_PROMPT = """
Generate content based on:
Task: {original_task}
Style: {task_type}
Guidelines: {task_description}

Return only your response:
[Your content here, maintaining the specified style and fully addressing requirements.]
"""

task = """Write a product description for a new eco-friendly water bottle.
The target_audience is environmentally conscious millennials and key product features are: plastic-free, insulated, lifetime warranty
"""

class Task(BaseModel):
    type: Literal["formal", "conversational", "hybrid"]
    description: str

class TaskList(BaseModel):
    analysis: str
    tasks: List[Task]  = Field(..., default_factory=list)

async def orchestrator_workflow(task : str, orchestrator_prompt : str, worker_prompt : str): 
    """Use a orchestrator model to break down a task into sub-tasks and then use worker models to generate and return responses."""

    # Use orchestrator model to break the task up into sub-tasks
    orchestrator_response = JSON_llm(orchestrator_prompt.format(task=task), schema=TaskList)
 
    # Parse orchestrator response
    analysis = orchestrator_response["analysis"]
    tasks= orchestrator_response["tasks"]

    print("\n=== ORCHESTRATOR OUTPUT ===")
    print(f"\nANALYSIS:\n{analysis}")
    print(f"\nTASKS:\n{json.dumps(tasks, indent=2)}")

    worker_model =  ["gpt-4o"]*len(tasks)

    # Gather intermediate responses from worker models
    return tasks, await asyncio.gather(*[run_llm_parallel(prompt=worker_prompt.format(original_task=task, task_type=task_info['type'], task_description=task_info['description']), model=model) for task_info, model in zip(tasks,worker_model)])

async def main():
    task = """Write a product description for a new eco-friendly water bottle. 
    The target_audience is environmentally conscious millennials and key product features are: plastic-free, insulated, lifetime warranty
    """

    tasks, worker_resp = await orchestrator_workflow(task, orchestrator_prompt=ORCHESTRATOR_PROMPT, worker_prompt=WORKER_PROMPT)

    for task_info, response in zip(tasks, worker_resp):
       print(f"\n=== WORKER RESULT ({task_info['type']}) ===\n{response}\n")

asyncio.run(main())