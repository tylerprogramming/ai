#!/usr/bin/env python
import sys
from crew import AgenttestsCrew
import agentops

agentops.init()

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    result = AgenttestsCrew().crew().kickoff(inputs=inputs)
    print(result)

run()