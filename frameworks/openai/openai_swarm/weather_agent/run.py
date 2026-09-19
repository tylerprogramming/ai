from swarm.repl import run_demo_loop
from agents import weather_agent

# run the demo loop
# it has the while True loop that allows you to keep interacting with the agent
# stream=True allows for streaming responses
# it does make sure you have a valid city
if __name__ == "__main__":
    run_demo_loop(weather_agent, stream=True)