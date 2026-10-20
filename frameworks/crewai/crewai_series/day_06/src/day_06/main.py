#!/usr/bin/env python
import sys
from crew import Day06Crew
from dotenv import load_dotenv
import os

load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'meta ai'
    }

    Day06Crew().crew().kickoff(inputs=inputs)

run()