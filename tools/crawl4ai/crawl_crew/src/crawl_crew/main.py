#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import CrawlCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sitemap_url': 'https://docs.crewai.com/sitemap.xml'
    }
    
    try:
        CrawlCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()