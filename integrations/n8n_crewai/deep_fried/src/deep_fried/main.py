#!/usr/bin/env python
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from .crews.deep_fried_crew.deep_fried_crew import DeepFriedResponseCrew

class DeepFriedState(BaseModel):
    arrival_rating: int = 1
    comments: str = ""
    feedback: str = ""
    overall: int = 1
    timestamp: str = ""
    response: str = ""
    
class DeepFriedFlow(Flow[DeepFriedState]):
    @start()
    def log_state(self):
        print("Logging Deep Fried State")
        
        with open("log.txt", "a") as f:
            f.write(self.state.model_dump_json())

    @listen(log_state)
    def generate_response(self):
        print("Generating response")
        result = (
            DeepFriedResponseCrew()
            .crew()
            .kickoff(inputs={"arrival_rating": self.state.arrival_rating, "comments": self.state.comments, "feedback": self.state.feedback, "overall": self.state.overall, "timestamp": self.state.timestamp})
        )

        self.state.response = result.raw
        return self.state.response

# Sample feedback (the same shape n8n sends) so `kickoff` also works on its own
SAMPLE_DATA = {
    "arrival_rating": 3,
    "comments": "Please...no...",
    "feedback": "It wasn't even fried....",
    "overall": 2,
    "timestamp": "12/12/2024 16:46:12",
}


def kickoff(data=None):
    data = data or SAMPLE_DATA
    deep_fried_flow = DeepFriedFlow()
    result = deep_fried_flow.kickoff(inputs={
        "arrival_rating": data.get("arrival_rating"), 
        "comments": data.get("comments"), 
        "feedback": data.get("feedback"), 
        "overall": data.get("overall"), 
        "timestamp": data.get("timestamp")
    })
    
    return result

def plot():
    DeepFriedFlow().plot()


if __name__ == "__main__":
    kickoff()
