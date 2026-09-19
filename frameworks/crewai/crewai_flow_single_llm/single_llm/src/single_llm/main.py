import json
import os
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.flow import Flow, listen, start
from crewai import LLM
from prompts import create_workout_plan_prompt

from dotenv import load_dotenv

load_dotenv()

class WorkoutPlan(BaseModel):
    workout_plan: str = Field(description="Workout plan for a day")

class SingleLLMState(BaseModel):
    wake_up_time: str = ""
    bedtime: str = ""
    workout_active: str = ""
    run: str = ""
    workout_plan: str = ""
    output_path: str = "workout_plan_google.md"

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
        
        self.log(f"Great! I'll create a workout plan for you based on the following information:")
        self.log(f"Wake up time: {self.state.wake_up_time}")
        self.log(f"Bedtime: {self.state.bedtime}")
        self.log(f"Workout active: {self.state.workout_active}")
        self.log(f"Run: {self.state.run}")

    @listen(user_input)
    def create_guide_outline(self):
        messages = create_workout_plan_prompt(
            self.state.wake_up_time, 
            self.state.bedtime, 
            self.state.workout_active, 
            self.state.run
        )
        
        # llm = LLM(
        #     model="openai/gpt-4o", 
        #     response_format=WorkoutPlan
        # )
        google_llm = LLM(
            model="gemini/gemini-2.5-flash-preview-04-17",
            api_key=os.getenv("GEMINI_API_KEY"),
            response_format=WorkoutPlan
        )
        
        response = google_llm.call(messages=messages)

        self.state.workout_plan = response

        self.log(f"Here is your workout plan:")
        self.log(self.state.workout_plan)

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
            self.log("Error: Invalid JSON format")
        except Exception as e:
            self.log(f"Error saving workout plan: {str(e)}")

def kickoff():
    workout_flow = SingleLLMFlow()
    workout_flow.kickoff()

if __name__ == "__main__":
    kickoff()
