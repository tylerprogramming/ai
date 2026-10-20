# Day03 Crew

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

Welcome to the Day03 Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

```bash
poetry install
```

(or `uv sync`)

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/day_03/config/agents.yaml` to define your agents
- Modify `src/day_03/config/tasks.yaml` to define your tasks
- Modify `src/day_03/crew.py` to add your own logic, tools and specific args
- Modify `src/day_03/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run python src/day_03/main.py
```

This command initializes the day_03 Crew, assembling the agents and assigning them tasks as defined in your configuration.

It searches the news with Serper (set `SERPER_API_KEY` too) and writes a `report.md` file in the folder you run it from.

## Understanding Your Crew

The day_03 Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Day03 Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
