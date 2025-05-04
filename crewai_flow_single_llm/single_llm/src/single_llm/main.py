import json
import os
from pathlib import Path

from pydantic import BaseModel

from crewai.flow import Flow, listen, start
from crewai import LLM
from pydantic import Field

class WorkoutPlan(BaseModel):
    workout_plan: str = Field(description="Workout plan for a day")

class SingleLLMState(BaseModel):
    wake_up_time: str = ""
    bedtime: str = ""
    workout_active: str = ""
    run: str = ""
    workout_plan: str = ""
    output_path: str = "workout_plan.md"

class SingleLLMFlow(Flow[SingleLLMState]):
    
    def log(self, message):
        print(message)

    @start()
    def user_input(self):
        wake_up_time = input("When do you wake up?: ")
        bedtime = input("When do you go to bed?: ")
        workout_active = input("How often do you work out?: ")
        run = input("How often do you run?: ")
        
        self.state.wake_up_time = wake_up_time
        self.state.bedtime = bedtime
        self.state.workout_active = workout_active
        self.state.run = run

    @listen(user_input)
    def create_guide_outline(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output workout plans."},
            {"role": "user", "content": f"""
            Create a workout plan for a day based on the following information:
            - Wake up time: {self.state.wake_up_time}
            - Bedtime: {self.state.bedtime}
            - Workout active: {self.state.workout_active}
            - Run: {self.state.run}
            
            Only return the workout plan, nothing else.
            """}
        ]
        llm = LLM(model="openai/gpt-4o", response_format=WorkoutPlan)
        response = llm.call(messages=messages)

        self.state.workout_plan = response

    @listen(create_guide_outline)
    def save_workout_plan(self):
        try:
            # Parse the JSON string
            if isinstance(self.state.workout_plan, str):
                workout_data = json.loads(self.state.workout_plan)
            else:
                workout_data = self.state.workout_plan
                
            # Extract the workout plan
            workout_plan = workout_data.get("workout_plan", "")
            
            # Ensure the output directory exists
            output_dir = os.path.dirname(self.state.output_path)
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
            # Write the workout plan to a markdown file
            with open(self.state.output_path, 'w') as f:
                f.write("# Daily Workout Plan\n\n")
                f.write(workout_plan)
            
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
        except Exception as e:
            print(f"Error saving workout plan: {str(e)}")

def kickoff():
    workout_flow = SingleLLMFlow()
    workout_flow.kickoff()

if __name__ == "__main__":
    kickoff()
