#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from work_out_flow.crews.workout_crew.workout_crew import WorkOutCrew

class WorkOutState(BaseModel):
    sentence_count: int = 1
    workout: str = ""

class WorkOutFlow(Flow[WorkOutState]):

    @start()
    def create_drive_folder(self):
        print("Creating drive folder")
        self.state.drive_folder = randint(1, 5)

    @listen(create_drive_folder)
    def research_workouts(self):
        print("Researching workouts")
        result = (
            WorkOutCrew()
            .crew()
            .kickoff(inputs={"drive_folder": self.state.drive_folder})
        )

        print("Workouts researched", result.raw)
        self.state.workout = result.raw

    @listen(research_workouts)
    def summarize_workouts(self):
        print("Summarizing workouts")
        result = (
            WorkOutCrew()
            .crew()
            .kickoff(inputs={"workout": self.state.workout})
        )
        print("Workouts summarized", result.raw)
        self.state.workout = result.raw

    @listen(summarize_workouts)
    def create_workout_plan(self):
        print("Creating workout plan")
        result = (
            WorkOutCrew()
            .crew()
            .kickoff(inputs={"workout": self.state.workout})
        )
        print("Workout plan created", result.raw)
        self.state.workout = result.raw

    @listen(create_workout_plan)
    async def send_workout_plan(self):
        print("Sending workout plan")
        result = (
            WorkOutCrew()
            .crew()
            .kickoff(inputs={"workout": self.state.workout})
        )
        print("Workout plan sent", result.raw)
        self.state.workout = result.raw
        
    @listen(send_workout_plan)
    async def send_slack_message(self):
        print("Sending slack message")
        result = (
            WorkOutCrew()
            .crew()
            .kickoff(inputs={"workout": self.state.workout})
        )
        print("Slack message sent", result.raw)
        self.state.workout = result.raw
        
def kickoff():
    workout_flow = WorkOutFlow()
    workout_flow.kickoff()


def plot():
    workout_flow = WorkOutFlow()
    workout_flow.plot()


if __name__ == "__main__":
    kickoff()
