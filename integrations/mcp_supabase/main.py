from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from telegram_messaging import send_telegram_message
from dotenv import load_dotenv

import time
import os

load_dotenv()

def background_supabase_task():
    print(f"Function executed at {datetime.now()}")
    # Create a StdioServerParameters object
    server_params=StdioServerParameters(
        command="npx", 
        args=[
            "-y",
            "@supabase/mcp-server-supabase@latest",
            "--access-token",
            os.getenv("SUPABASE_ACCESS_TOKEN")
        ],
    )

    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")

        # Example: Using the tools from the Stdio MCP server in a CrewAI Agent
        research_agent = Agent(
            role="Supabase Agent",
            goal="Get the latest records from the database.",
            backstory="You are an agent for supabase for getting the latest records from the database.",
            tools=tools,
            reasoning=True,
            verbose=True,
        )
        
        processing_task = Task(
            description="""
                Retrieve the last 5 records from the database.  
                The project is fullstack-app.
                The table is called habits. 

                I just need you to take the habits for the day and give a quote from Atomic Habits by James Clear.
                
                Summarize concisely the habits and quote.  Also format nicely for telegram.
            """,
            expected_output="The summarize habits for the day and quote from Atomic Habits by James Clear formatted ONLY.",
            agent=research_agent,
            markdown=True
        )
        
        data_crew = Crew(
            agents=[research_agent],
            tasks=[processing_task],
            verbose=True,
            process=Process.sequential 
        )
    
        result = data_crew.kickoff()
        print(result)
        send_telegram_message(result.raw)
        
        print("\nCrew Task Result (Stdio - Managed):\n", result)


# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(background_supabase_task, 'cron', hour=23, minute=18)
scheduler.start()

try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()