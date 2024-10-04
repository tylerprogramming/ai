from main_crew import MyCrew
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['OPENAI_API_KEY'] = 'insert openai api key here'

def run_crew():
    result = MyCrew().crew().kickoff()
    print(result)
    
run_crew()