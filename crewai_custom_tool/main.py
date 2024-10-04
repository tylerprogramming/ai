from custom_tool_crew import NewsAggregationCrew
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

os.environ['OPENAI_API_KEY'] = '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'

def run_crew():
    inputs = {
        'topic': 'latest ai news',
        'date': datetime.now().strftime("%Y-%m-%d")
    }

    result = NewsAggregationCrew().crew().kickoff(inputs=inputs)
    crew_output = result.to_dict()
    print(crew_output)
    
run_crew()