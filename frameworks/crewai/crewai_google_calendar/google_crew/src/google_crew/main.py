#!/usr/bin/env python
import os
import sys
import warnings

from datetime import datetime

try:
    from google_crew.crew import GoogleCrew  # `crewai run` (installed package)
except ImportError:
    from crew import GoogleCrew  # `python src/google_crew/main.py`

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    # Who gets the confirmation email: set RECIPIENT_EMAIL in .env
    recipient = os.getenv("RECIPIENT_EMAIL", "you@example.com")
    inputs = {
        'query': f'I want to create a daily standup meeting in the calendar for these days: monday through thursday from 2pm - 2:15 pm titled Catchup - Standup.  Just make sure these slots are available, and if they are, then creat them.  Then send an email to {recipient}.',
        'current_date': str(datetime.now().date())
    }
    
    try:
        return GoogleCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    result = run()
    print(result)
