from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os
import sys
import warnings
from pydantic import PydanticDeprecatedSince20
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# The folder the filesystem MCP server is allowed to read/write (change it to e.g. your Downloads folder)
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def env_from(*names):
    """Pass only the env vars that are set (a None value would crash the server launch)."""
    return {name: os.environ[name] for name in names if os.getenv(name)}


server_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        DOWNLOADS_DIR,
    ],
)

# Note: this npm package is deprecated (still runs). GitHub's official server is github/github-mcp-server
# (Docker image ghcr.io/github/github-mcp-server, or the remote server at https://api.githubcopilot.com/mcp/).
github_server_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-github",
    ],
    env=env_from("GITHUB_PERSONAL_ACCESS_TOKEN"),
)
      

brave_search_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@brave/brave-search-mcp-server",  # Brave's official server (replaces @modelcontextprotocol/server-brave-search)
    ],
    env=env_from("BRAVE_API_KEY"),
)

image_server_params=StdioServerParameters(
    command=sys.executable,  # same Python (and venv) as this script
    args=[
        os.path.join(BASE_DIR, "servers", "image_server.py"),
    ],
    env=env_from("OPENAI_API_KEY", "OPENAI_ORGANIZATION"),
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