# Day05 Crew

Welcome to the Day05 Crew project, powered by [crewAI](https://crewai.com). This project demonstrates how to set up a multi-agent AI system for automated content creation and marketing strategy development.

## Project Overview

The Day05 Crew project focuses on creating an automated workflow for developing a comprehensive content marketing strategy. It utilizes multiple AI agents, each with specific roles and responsibilities, to collaborate on tasks related to content ideation, creation, and marketing strategy development.

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

The main components of the Day05 Crew project are located in the `src/day_05` directory:

- `config/agents.yaml`: Defines the AI agents and their roles (e.g., Content Strategist, Writer, Editor).
- `config/tasks.yaml`: Specifies the tasks to be performed by the agents.
- `crew.py`: Sets up the CrewAI workflow and integrates agents and tasks.
- `main.py`: The entry point of the application, orchestrating the entire process.
- `tools.py`: Contains custom tools used by the agents, such as content research and SEO analysis.

## Running the Project

To start the content marketing strategy development process, run this command from the root folder of your project:

```bash
poetry run python src/day_05/main.py
```

This command initializes the Day05 Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The Day05 Crew consists of multiple AI agents, each with unique roles:

1. Content Strategist: Develops overall content strategy and identifies target audience.
2. Writer: Creates engaging content based on the strategy.
3. Editor: Reviews and refines the content for quality and consistency.
4. SEO Specialist: Optimizes content for search engines and provides keyword recommendations.
5. Social Media Manager: Develops a plan for content distribution across various platforms.

These agents collaborate on a series of tasks defined in `config/tasks.yaml`, leveraging their collective skills to produce a comprehensive content marketing strategy.

## Output

The project generates a `content_marketing_strategy.md` file in the root directory, containing the final content marketing strategy produced by the AI agents. This includes content ideas, SEO recommendations, and a social media distribution plan.

## Support

For support, questions, or feedback regarding the Day05 Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Explore the power of automated content marketing strategy development with crewAI!
