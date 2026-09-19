# Day04 Crew

Welcome to the Day04 Crew project, powered by [crewAI](https://crewai.com). This project demonstrates how to set up a multi-agent AI system for automated news analysis and report generation.

## Project Overview

The Day04 Crew project focuses on creating an automated workflow for analyzing news articles and generating comprehensive reports. It utilizes multiple AI agents, each with specific roles and responsibilities, to collaborate on tasks related to news gathering, analysis, and report writing.

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

The main components of the Day04 Crew project are located in the `src/day_04` directory:

- `config/agents.yaml`: Defines the AI agents and their roles.
- `config/tasks.yaml`: Specifies the tasks to be performed by the agents.
- `crew.py`: Sets up the CrewAI workflow and integrates agents and tasks.
- `main.py`: The entry point of the application, orchestrating the entire process.
- `tools.py`: Contains custom tools used by the agents, such as web scraping and file operations.

## Running the Project

To start the news analysis and report generation process, run this command from the root folder of your project:

```bash
poetry run python src/day_04/main.py
```

This command initializes the Day04 Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The Day04 Crew consists of multiple AI agents, each with unique roles:

1. News Researcher: Gathers and summarizes relevant news articles.
2. Data Analyst: Analyzes the collected news data for trends and insights.
3. Report Writer: Compiles the analysis into a comprehensive report.

These agents collaborate on a series of tasks defined in `config/tasks.yaml`, leveraging their collective skills to produce a final news analysis report.

## Output

The project generates a `news_report.md` file in the root directory, containing the final news analysis report produced by the AI agents.

## Support

For support, questions, or feedback regarding the Day04 Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Explore the power of automated news analysis with crewAI!
