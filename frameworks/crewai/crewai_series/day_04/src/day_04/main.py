#!/usr/bin/env python
import sys
from crew import Day04Crew
from datetime import datetime

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'ai agents'
    }

    Day04Crew().crew().kickoff(inputs=inputs)

run()