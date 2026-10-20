#!/usr/bin/env python
import sys
from crew import Day03Crew
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'openai',
        'date': datetime.now().strftime("%Y-%m-%d")
    }
    Day03Crew().crew().kickoff(inputs=inputs)

run()