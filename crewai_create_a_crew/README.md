## Description

This CrewAI project consists of two main components:

1. A joke generator agent
2. An emoji enhancement agent

The system works sequentially, first generating a joke and then enhancing it with emojis.

## Files

### main_crew.py

This file defines the `MyCrew` class, which sets up the agents and tasks for the CrewAI system.

### run_crew.py

This script initializes and runs the CrewAI system, printing the final result.

### config/agents.yaml

This configuration file defines the roles, goals, and backstories for the two agents:

- `my_agent`: Responsible for generating witty jokes
- `emoji_agent`: Responsible for adding emojis to enhance the jokes

### config/tasks.yaml

This configuration file defines the tasks for the CrewAI system:

- `my_task`: Generate a new and funny joke
- `emoji_task`: Add emojis to the generated joke

## Usage

1. Ensure you have the required dependencies installed:
   ```
   pip install crewai python-dotenv
   ```

2. Set up your OpenAI API key in a `.env` file or as an environment variable.

3. Run the system:
   ```
   python run_crew.py
   ```

The system will generate a joke and enhance it with emojis, then print the result.

## Customization

You can modify the `agents.yaml` and `tasks.yaml` files to adjust the behavior of the agents or change the tasks they perform. The `main_crew.py` file can be extended to add more agents or tasks as needed.

## Note

Make sure to keep your API keys secure and never commit them to version control.