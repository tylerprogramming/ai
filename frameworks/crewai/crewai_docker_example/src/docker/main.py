#!/usr/bin/env python
import sys
try:
    from docker.crew import DockerCrew  # `crewai run` (installed package)
except ImportError:
    from crew import DockerCrew  # `python src/docker/main.py` (used by the Dockerfile)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    DockerCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
