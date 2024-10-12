# Day06 Crew

Welcome to the Day06 Crew project, powered by [crewAI](https://crewai.com). This project demonstrates how to set up a multi-agent AI system for automated task execution in a software development context.

## Project Overview

The Day06 Crew project focuses on creating an automated workflow for executing a series of tasks related to news analysis and report generation. It utilizes the new Flow system from CrewAI.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

```bash
poetry install
```

### Configuration

**Add your `OPENAI_API_KEY` into the `.env` file**

## Project Structure

The main components of the Day06 Crew project are located in the `src/day_06` directory:

- `workflow.py`: Defines the workflow class and task execution logic.
- `main.py`: The entry point of the application, setting up the workflow and running the tasks.

## Running the Project

To start the automated task execution process, run this command from the root folder of your project:

```bash
poetry run python src/day_06/main.py
```

This command initializes the Day06 Crew, setting up the workflow and executing the defined tasks.

## Understanding Your Workflow

The Day06 project implements a workflow with the following key features:

1. Multiple Crews.
2. Multiple Agent and Task yaml files for different crews.
3. Sequential execution of tasks, with each task building upon the results of the previous ones.
4. Ability to pass context and results between tasks.
5. Plotting the workflow using the `flow.plot()` method.

The workflow is designed to be flexible and can be easily modified to include different tasks or change the execution order.

## Output

The project generates output for each task executed in the workflow. The specific output depends on the tasks defined, but it may include:

- AI news/markdown reports

The output is typically displayed in the console as the workflow progresses.

## Support

For support, questions, or feedback regarding the Day06 Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Experience the power of automated task execution in software development with crewAI!
