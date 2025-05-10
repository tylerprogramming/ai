from openai import OpenAI
import base64
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    organization=os.getenv("OPENAI_ORGANIZATION")
)

prompt = """
    
import os

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_
from crewai import Agent, Task, Crew, LLM
from composio_crewai import ComposioToolSet, Action, App

from crews.research_crew.research_crew import ResearchCrew
from crews.summary_crew.summary_crew import SummaryCrew

from dotenv import load_dotenv

load_dotenv()

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
google_create_find_folder = composio_toolset.get_tools(actions=['GOOGLEDRIVE_CREATE_FOLDER', 'GOOGLEDRIVE_FIND_FOLDER', 'GOOGLEDRIVE_DELETE_FOLDER_OR_FILE'])
google_upload_file = composio_toolset.get_tools(actions=['GOOGLEDRIVE_FIND_FOLDER', 'GOOGLEDRIVE_UPLOAD_FILE', 'GOOGLEDRIVE_CREATE_FILE_FROM_TEXT'])
slack_toolset = composio_toolset.get_tools(actions=['SLACK_SENDS_A_MESSAGE_TO_A_SLACK_CHANNEL'])

openai_llm = LLM(model="gpt-4o", temperature=0)

class WorkOutResearch(BaseModel):
    research: str = ""
    links: list[str] = []

class DriveFolder(BaseModel):
    id: str = ""
    name: str = ""
    parent_id: str = ""
    created_at: str = ""

class WorkOutState(BaseModel):
    drive_folder_id: str = ""
    drive_folder: str = "Workout"
    doc_file_path: str = "workout_plan.docx"
    csv_file_path: str = "workout_plan.csv"
    workout: str = ""
    csv_workout: str = ""
    research: WorkOutResearch = WorkOutResearch()
    summary: str = ""
    
class WorkOutFlow(Flow[WorkOutState]):

    @start()    
    def create_or_retrieve_drive_folder(self):
        # Define agent
        crewai_agent = Agent(
            role="Google Drive Agent",
            goal="You are an AI agent that is responsible for taking actions based on the tools you have",
            backstory=(
                "You are an AI agent that is responsible for taking actions based on the tools you have"
            ),
            verbose=True,
            tools=google_create_find_folder,
            llm=openai_llm
        )
        task = Task(
            description=f"Check if there is a folder called {self.state.drive_folder}.  If there is no folder,then create a new folder in Google Drive called {self.state.drive_folder}.  There is no parent folder so it should be empty, this is the root.",
            agent=crewai_agent,
            expected_output="Just the id of the folder"
        )
        my_crew = Crew(agents=[crewai_agent], tasks=[task])

        result = my_crew.kickoff()
        
        self.state.drive_folder_id = result.raw

    @listen(create_or_retrieve_drive_folder)
    def research_workouts(self):
        result = (
            ResearchCrew()
            .crew()
            .kickoff()
        )

        self.state.research = result.pydantic

    @listen(research_workouts)
    def summarize_workouts(self):
        result = (
            SummaryCrew()
            .crew()
            .kickoff(inputs={"workout": self.state.workout})
        )

        self.state.summary = result.raw

    @listen(summarize_workouts)
    async def create_doc_workout_plan(self, workout: str):
        crewai_agent = Agent(
            role="Workout Plan Agent",
            goal="You are an AI agent that is responsible for creating a workout plan.",
            backstory=(
                "You are an AI agent that is responsible for creating a workout plan"
            ),
            verbose=True,
            llm=openai_llm
        )
        task = Task(
            description=f"Create a workout plan based on the following information: {workout}.  The workout plan shouldn't be in markdown format, it should be in a format that can be easily read by a human for a word document.",
            agent=crewai_agent,
            expected_output="A workout plan in a format that can be easily read by a human for a word document."
        )
        my_crew = Crew(agents=[crewai_agent], tasks=[task])
        result = my_crew.kickoff()
        
        self.state.workout = result.raw
        
    @listen(summarize_workouts)
    async def create_csv_workout_plan(self, workout: str):
        crewai_agent = Agent(
            role="Workout Plan Agent",
            goal="You are an AI agent that is responsible for creating a workout plan.",
            backstory=(
                "You are an AI agent that is responsible for creating a workout plan"
            ),
            verbose=True,
            llm=openai_llm
        )
        task = Task(
            description=f"Create a workout plan based on the following information: {workout}.  The workout plan should be in a csv format.  Also give days of the week, and how many reps per workout for each day.  Make sure the csv is as detailed as possible.",
            agent=crewai_agent,
            expected_output="The whole workout plan in a csv format."
        )
        my_crew = Crew(agents=[crewai_agent], tasks=[task])
        result = my_crew.kickoff()
        
        self.state.csv_workout = result.raw

    @listen(and_(create_doc_workout_plan, create_csv_workout_plan))
    def save_workout_plan(self):
        crewai_agent = Agent(
            role="Google Drive Agent",
            goal="You are an AI agent that is responsible for taking actions based on the tools you have",
            backstory=(
                "You are an AI agent that is responsible for taking actions based on the tools you have"
            ),
            verbose=True,
            tools=google_upload_file,
            llm=openai_llm
        )
        task = Task(
            description=f"Create two files: {self.state.doc_file_path} with the content {self.state.workout} and then {self.state.csv_file_path} with the content: {self.state.csv_workout}, and the parent folder id: {self.state.drive_folder_id} for both files.",
            agent=crewai_agent,
            expected_output="If it was successful or not."
        )
        
        my_crew = Crew(agents=[crewai_agent], tasks=[task])
        my_crew.kickoff()
        
    @listen(save_workout_plan)
    async def send_slack_message(self):
        crewai_agent = Agent(
            role="Slack Agent",
            goal="You are an AI agent that is responsible for taking actions based on the tools you have",
            backstory=(
                "You are AI agent that is responsible for taking actions based on the tools you have"
            ),
            verbose=True,
            tools=slack_toolset,
            llm=openai_llm,
        )
        task = Task(
            description=f"Send a message to the Slack channel #general with the workout plan: {self.state.workout}",
            agent=crewai_agent,
            expected_output="The message sent"
        )
        my_crew = Crew(agents=[crewai_agent], tasks=[task])
        my_crew.kickoff()
        
def kickoff():
    workout_flow = WorkOutFlow()
    workout_flow.plot()
    workout_flow.kickoff()

if __name__ == "__main__":
    kickoff()

"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("images_output/image_gen1.png", "wb") as f:
    f.write(image_bytes)
    
    
    
    
