from custom_tool_crew import NewsAggregationCrew
from dotenv import load_dotenv
import os
from datetime import datetime
import agentops
from agentops.enums import EndState
import schedule
import time

load_dotenv()

os.environ['OPENAI_API_KEY'] = 'insert api key'
session = agentops.init(api_key="insert api key")

def run_crew():
    inputs = {
        'topic': 'latest ai news',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    NewsAggregationCrew().crew().kickoff(inputs=inputs)

    session.end_session(end_state=EndState.SUCCESS)

def schedule_crew():
    # schedule.every(2).minutes.do(run_crew)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    run_crew()

if __name__ == "__main__":
    schedule_crew()