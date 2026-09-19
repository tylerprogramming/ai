#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import GoogleCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'query': 'I want to create a daily standup meeting in the calendar for these days: monday through thursday from 2pm - 2:15 pm titled Catchup - Standup.  Just make sure these slots are available, and if they are, then creat them.  Then send an email to tylerreed8893@gmail.com.',
        'current_date': str(datetime.now().date())
    }
    
    try:
        return GoogleCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    result = run()
    print(result)
