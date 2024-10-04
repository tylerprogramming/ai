# CrewAI GPT Local

This project demonstrates the use of CrewAI to create a Chuck Norris joke generation system using local language models and LM Studio.

## Overview

The system consists of three main components:

1. A Chuck Norris fact-finding agent
2. A Chuck Norris joke picker
3. A Chuck Norris joke creator

These components work together in a sequential process to generate Chuck Norris jokes.

## Files

- `main-lmstudio.py`: The main script that sets up and runs the CrewAI system using LM Studio.
- `main-ollama.py`: An alternative main script that uses Ollama for local language models.
- `main-local-ollama-lmstudio.py`: A combined script that can use both Ollama and LM Studio.
- `main-gpt.py`: A version that uses OpenAI's GPT models (requires API key).
- `config/agents.yaml`: Configuration file for the agents.
- `config/tasks.yaml`: Configuration file for the tasks.

## How it works

1. The `ChuckNorrisCrew` class is defined as a `CrewBase`, which sets up the agents and tasks.

2. Three agents are created:
   - `chuck_norris_agent`: Finds Chuck Norris facts using the SerperDevTool.
   - `chuck_norris_jokes_picker`: Selects the best Chuck Norris jokes.
   - `chuck_norris_joke_creator`: Creates new Chuck Norris jokes.

3. Three corresponding tasks are defined for each agent.

4. The crew is set up with these agents and tasks, using a sequential process.

5. When the script is run, it creates an instance of `ChuckNorrisCrew` and kicks off the process.

## Usage

1. Ensure you have the required dependencies installed:
   ```
   pip install crewai langchain-community python-dotenv
   ```

2. Set up your environment variables in a `.env` file if necessary.

3. Run the desired main script:
   ```
   python main-lmstudio.py
   ```

   Or for Ollama:
   ```
   python main-ollama.py
   ```

4. The script will output the result of the CrewAI process, which should be a Chuck Norris joke.

## Customization

You can modify the `agents.yaml` and `tasks.yaml` files in the `config` folder to adjust the behavior of the agents and tasks. You can also modify the main script to use different language models or add new agents and tasks as needed.

## Note

This project uses local language models through LM Studio and Ollama. Make sure you have these set up and running on your local machine before running the scripts.