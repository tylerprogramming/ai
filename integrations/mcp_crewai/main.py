from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os
import warnings
from pydantic import PydanticDeprecatedSince20
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

server_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tylerreed/Downloads",
    ],
)

github_server_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-github",
    ],
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")},
)
      

brave_search_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-brave-search",
    ],
    env={"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")},
)

image_server_params=StdioServerParameters(
    command="python3",
    args=[
        "servers/image_server.py",
    ],
    env={"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"), "OPENAI_ORGANIZATION": os.getenv("OPENAI_ORGANIZATION")},
)

all_tools=[server_params, brave_search_params, image_server_params, github_server_params]
with MCPServerAdapter(all_tools) as tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")

    # Example: Using the tools from the Stdio MCP server in a CrewAI Agent
    agent = Agent(
        role="Creator",
        goal="You are an amazing AI Creator who uses MCP Tools.",
        backstory="An AI that can create images via an MCP tool.",
        tools=tools,
        verbose=True,
    )
    
    task = Task(
        description="""I need you to research Model Context Protocol and create an in-depth diagram on how it works.""",
        expected_output="A summary of the brave search results and a successful image creation.",
        agent=agent,
    )
    
    summary_task = Task(
        description="Summarize the results of the task and create a text file in the downloads folder (check allowed folders) and save the summary to this file.",
        expected_output="A summary of the brave search results in a text file in the downloads folder.",
        agent=agent,
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task, summary_task],
        verbose=True,
    )
    result = crew.kickoff()
    print(result)