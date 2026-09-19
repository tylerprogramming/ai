from smolagents import CodeAgent, VisitWebpageTool, HfApiModel, Tool

from dotenv import load_dotenv

load_dotenv()

get_travel_duration_tool = Tool.from_space(
    "m-ric/get-travel-duration-tool",
    name="get_travel_duration_tool",
    description="Get the travel duration between two locations"
)

response = get_travel_duration_tool("Paris", "London")
print(response)