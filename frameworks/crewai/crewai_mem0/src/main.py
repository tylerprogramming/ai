#!/usr/bin/env python
import sys
from crew import Mem0Crew

def run():
    """
    Run the crew.
    """

    result = Mem0Crew().crew().kickoff()
    print(result)

if __name__ == "__main__":
    run()
