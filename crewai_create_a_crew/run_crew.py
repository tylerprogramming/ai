from main_crew import MyCrew
from dotenv import load_dotenv
import os
import agentops
from agentops.enums import EndState

load_dotenv()

os.environ['OPENAI_API_KEY'] = 'insert api key'
session = agentops.init(api_key="insert api key")

def run_crew():
    # agentops.session.Session.record()
    result = MyCrew().crew().kickoff()
    print(result)
    session.end_session(end_state=EndState.SUCCESS)
    
run_crew()