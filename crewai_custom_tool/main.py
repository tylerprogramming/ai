from custom_tool_crew import NewsAggregationCrew
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

os.environ['OPENAI_API_KEY'] = 'insert openai api key here'

def run_crew():
    inputs = {
        'topic': 'latest ai news',
        'date': datetime.now().strftime("%Y-%m-%d")
    }

    result = NewsAggregationCrew().crew().kickoff(inputs=inputs)
    crew_output = result.to_dict()
    print(crew_output)
    
run_crew()