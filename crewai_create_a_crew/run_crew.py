from main_crew import MyCrew
from dotenv import load_dotenv
import os
import agentops
from agentops.enums import EndState

load_dotenv()

os.environ['OPENAI_API_KEY'] = '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'
session = agentops.init(api_key="42818d52-a7c0-49ff-a086-be73a53543a1")

def run_crew():
    # agentops.session.Session.record()
    result = MyCrew().crew().kickoff()
    print(result)
    session.end_session(end_state=EndState.SUCCESS)
    
run_crew()